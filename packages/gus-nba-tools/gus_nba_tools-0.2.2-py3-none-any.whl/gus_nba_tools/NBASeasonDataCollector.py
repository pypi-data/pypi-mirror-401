
import pandas as pd
from nba_api.stats.endpoints import leaguedashplayerstats
import time
from typing import List, Optional


class NBASeasonDataCollector:
    """
    A class for collecting and processing NBA player statistics across multiple seasons.
    
    Combines NBA API per-100 possession stats with Basketball Reference position data,
    categorizing players into Guard/Wing/Big positions.
    
    Attributes:
        start_season (int): Starting season year (e.g., 2015 for 2015-16 season)
        end_season (int): Ending season year (e.g., 2024 for 2024-25 season)
        min_minutes (int): Minimum total minutes threshold (GP * MIN)
        sleep_duration (float): Delay between NBA API calls to avoid rate limiting
    """
    
    def __init__(
        self,
        start_season: int,
        end_season: int,
        min_minutes: int = 1000,
        sleep_duration: float = 1.5
    ):
        """
        Initialize the NBA Season Data Collector.
        
        Args:
            start_season: Starting season year (e.g., 2015 for 2015-16)
            end_season: Ending season year (e.g., 2024 for 2024-25)
            min_minutes: Minimum GP * MIN threshold for player inclusion (default: 1000)
            sleep_duration: Seconds to sleep between API calls (default: 1.5)
        """
        self.start_season = start_season
        self.end_season = end_season
        self.min_minutes = min_minutes
        self.sleep_duration = sleep_duration
        self.all_seasons_data: List[pd.DataFrame] = []
    
    @staticmethod
    def map_gwb_from_bbref(pos: str) -> Optional[str]:
        """
        Map Basketball-Reference 'Pos' values to Guard / Wing / Big.
        
        BBRef positions include:
          PG, SG, SF, PF, C,
          SG-SF, SF-PF, PF-C, C-PF, etc.
        
        Mapping:
          Guard -> PG, SG, PG-SG, SG-PG, G
          Wing  -> SF, SG-SF, SF-SG, G-F, F-G, F
          Big   -> PF, C, PF-C, C-PF, F-C, C-F
        
        Args:
            pos: Position string from Basketball Reference
            
        Returns:
            One of "Guard", "Wing", "Big", or None
        """
        if pd.isna(pos):
            return None
        
        pos = str(pos).upper().strip()
        parts = pos.split('-')
        primary = parts[0]
        
        guard_codes = {"PG", "SG", "G"}
        wing_codes = {"SF", "F"}
        big_codes = {"PF", "C"}
        
        if primary in guard_codes:
            return "Guard"
        elif primary in big_codes:
            return "Big"
        elif primary in wing_codes:
            return "Wing"
        else:
            if any(p in guard_codes for p in parts):
                return "Guard"
            if any(p in big_codes for p in parts):
                return "Big"
            return "Wing"
    
    @staticmethod
    def clean_nba_name(name: str) -> str:
        """Clean NBA player name for matching."""
        return str(name).strip()
    
    def get_nba_per100_base(self, season_str: str) -> pd.DataFrame:
        """
        Get per-100 possessions basic box score stats from nba_api.
        
        Args:
            season_str: Season string (e.g., "2015-16")
            
        Returns:
            DataFrame with basic per-100 stats
        """
        stats = leaguedashplayerstats.LeagueDashPlayerStats(
            season=season_str,
            per_mode_detailed="Per100Possessions",
            measure_type_detailed_defense="Base",
            timeout=60,
        )
        df = stats.get_data_frames()[0]
        
        keep = [
            "PLAYER_ID", "PLAYER_NAME", "TEAM_ID", "GP", "MIN",
            "PTS", "REB", "AST", "STL", "BLK", "TOV",
            "FG_PCT", "FG3_PCT", "FT_PCT",
            "FGA", "FG3A",
        ]
        df = df[keep]
        return df
    
    def get_nba_per100_advanced(self, season_str: str) -> pd.DataFrame:
        """
        Get per-100 possessions advanced stats from nba_api.
        
        Args:
            season_str: Season string (e.g., "2015-16")
            
        Returns:
            DataFrame with advanced per-100 stats
        """
        print(f"  - Fetching NBA advanced Per100 stats for {season_str}...")
        adv = leaguedashplayerstats.LeagueDashPlayerStats(
            season=season_str,
            per_mode_detailed="Per100Possessions",
            measure_type_detailed_defense="Advanced",
            timeout=60,
        )
        df = adv.get_data_frames()[0]
        
        possible_cols = [
            "PLAYER_ID",
            "USG_PCT", "AST_PCT", "REB_PCT", "OREB_PCT", "DREB_PCT",
            "TS_PCT", "EFG_PCT",
            "STL_PCT", "BLK_PCT", "TOV_PCT",
            "OFF_RATING", "DEF_RATING", "NET_RATING",
        ]
        keep = [c for c in possible_cols if c in df.columns]
        df = df[keep]
        return df
    
    def get_bbref_positions(self, end_year: int) -> pd.DataFrame:
        """
        Get BBRef per-game table for a season end year, extract Player and Pos.
        
        Args:
            end_year: Season end year (e.g., 2016 for 2015-16 season)
            
        Returns:
            DataFrame with player names and positions
        """
        url = f"https://www.basketball-reference.com/leagues/NBA_{end_year}_per_game.html"
        print(f"  - Fetching BBRef positions from {url}...")
        tables = pd.read_html(url)
        df = tables[0]
        
        # Remove header rows that repeat (Player == "Player")
        df = df[df["Player"] != "Player"]
        
        df = df[["Player", "Pos"]].copy()
        
        # Clean names (remove * suffix for All-Stars, etc.)
        df["Player_clean"] = (
            df["Player"]
            .str.replace(r"\*", "", regex=True)
            .str.strip()
        )
        
        return df
    
    def build_season_dataset(self, start_year: int) -> pd.DataFrame:
        """
        Build a dataset for one season.
        
        Args:
            start_year: Season start year (e.g., 2015 for 2015-16)
            
        Returns:
            DataFrame with combined NBA and BBRef data for the season
        """
        end_year = start_year + 1
        season_str = f"{start_year}-{str(end_year)[-2:]}"
        
        print(f"\nBuilding dataset for {season_str}...")
        
        # NBA per-100 base stats
        base_df = self.get_nba_per100_base(season_str)
        time.sleep(self.sleep_duration)
        
        # NBA per-100 advanced stats
        adv_df = self.get_nba_per100_advanced(season_str)
        time.sleep(self.sleep_duration)
        
        # Merge NBA stats on PLAYER_ID
        nba_df = base_df.merge(adv_df, on="PLAYER_ID", how="left")
        
        # Clean NBA player names for merge
        nba_df["Player_clean"] = nba_df["PLAYER_NAME"].apply(self.clean_nba_name)
        
        # BBRef positions for that season
        bbref_df = self.get_bbref_positions(end_year)
        
        # Merge NBA stats with BBRef positions on cleaned name
        merged = nba_df.merge(
            bbref_df[["Player_clean", "Pos"]],
            on="Player_clean",
            how="left",
        )
        
        # Drop rows with no position
        before_pos = len(merged)
        merged = merged.dropna(subset=["Pos"])
        after_pos = len(merged)
        print(f"  - Merged {after_pos}/{before_pos} players with BBRef positions.")
        
        # Map BBRef Pos -> Guard/Wing/Big
        merged["Position3"] = merged["Pos"].apply(self.map_gwb_from_bbref)
        
        # Filter by minutes played (GP * MIN >= threshold)
        merged = merged[merged["GP"] * merged["MIN"] >= self.min_minutes]
        print(f"  - After minutes filter: {len(merged)} players remain.")
        
        # Drop helper column
        merged = merged.drop(columns=["Player_clean"])
        
        return merged
    
    def collect_all_seasons(self, save_csv: bool = True) -> List[pd.DataFrame]:
        """
        Collect data for all seasons in the specified range.
        
        Args:
            save_csv: Whether to save individual season CSVs (default: True)
            
        Returns:
            List of DataFrames, one per season
        """
        self.all_seasons_data = []
        
        for yr in range(self.start_season, self.end_season + 1):
            try:
                df_season = self.build_season_dataset(yr)
                self.all_seasons_data.append(df_season)
                
                if save_csv:
                    filename = f"nba_{yr}_{yr+1}_per100_adv_gwb.csv"
                    df_season.to_csv(filename, index=False)
                    print(f"  - Saved: {filename}")
                    
            except Exception as e:
                print(f"!!! Error building season {yr}-{yr+1}: {e}")
        
        print(f"\nDone! Collected {len(self.all_seasons_data)} seasons.")
        return self.all_seasons_data
    
    def get_combined_data(self) -> pd.DataFrame:
        """
        Combine all collected seasons into a single DataFrame.
        
        Returns:
            Combined DataFrame with all seasons
        """
        if not self.all_seasons_data:
            raise ValueError("No data collected yet. Run collect_all_seasons() first.")
        
        return pd.concat(self.all_seasons_data, ignore_index=True)

