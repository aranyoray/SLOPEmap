"""
GeoID Generator Utility
Generates and validates GeoID ranges for NREL SLOPE county data
"""

class GeoIDGenerator:
    """Generate GeoID sequences for NREL SLOPE counties"""

    def __init__(self, start_id="G0100010", end_id="G5600450"):
        """
        Initialize GeoID generator

        Args:
            start_id (str): Starting GeoID (format: G + 7 digits)
            end_id (str): Ending GeoID (format: G + 7 digits)
        """
        self.start_id = start_id
        self.end_id = end_id

    @staticmethod
    def parse_geoid(geoid):
        """
        Parse GeoID string to integer

        Args:
            geoid (str): GeoID string (e.g., 'G0100010')

        Returns:
            int: Numeric portion of GeoID
        """
        if not geoid.startswith('G'):
            raise ValueError(f"Invalid GeoID format: {geoid}")
        return int(geoid[1:])

    @staticmethod
    def format_geoid(num):
        """
        Format integer to GeoID string

        Args:
            num (int): Numeric GeoID

        Returns:
            str: Formatted GeoID (e.g., 'G0100010')
        """
        return f"G{num:07d}"

    def generate_range(self, step=10):
        """
        Generate all GeoIDs in range with given step

        Args:
            step (int): Increment step for GeoIDs

        Yields:
            str: GeoID string
        """
        start_num = self.parse_geoid(self.start_id)
        end_num = self.parse_geoid(self.end_id)

        current = start_num
        while current <= end_num:
            yield self.format_geoid(current)
            current += step

    def get_batch(self, batch_size, offset=0):
        """
        Get a batch of GeoIDs

        Args:
            batch_size (int): Number of GeoIDs to return
            offset (int): Starting offset

        Returns:
            list: List of GeoID strings
        """
        geoids = list(self.generate_range())
        start_idx = offset
        end_idx = min(offset + batch_size, len(geoids))
        return geoids[start_idx:end_idx]

    def split_for_agents(self, num_agents):
        """
        Split GeoID range into chunks for multiple agents

        Args:
            num_agents (int): Number of agents to split work across

        Returns:
            list: List of (start_geoid, end_geoid) tuples for each agent
        """
        start_num = self.parse_geoid(self.start_id)
        end_num = self.parse_geoid(self.end_id)

        total_range = end_num - start_num
        chunk_size = total_range // num_agents

        agent_ranges = []
        for i in range(num_agents):
            chunk_start = start_num + (i * chunk_size)
            if i == num_agents - 1:
                # Last agent gets remainder
                chunk_end = end_num
            else:
                chunk_end = chunk_start + chunk_size - 1

            agent_ranges.append((
                self.format_geoid(chunk_start),
                self.format_geoid(chunk_end)
            ))

        return agent_ranges

    def count_total(self):
        """
        Count total number of GeoIDs in range

        Returns:
            int: Total count of GeoIDs
        """
        return len(list(self.generate_range()))


if __name__ == "__main__":
    # Example usage
    generator = GeoIDGenerator("G0100010", "G5600450")

    print(f"Total GeoIDs to scrape: {generator.count_total()}")
    print("\nFirst 10 GeoIDs:")
    for i, geoid in enumerate(generator.generate_range()):
        if i >= 10:
            break
        print(f"  {geoid}")

    print("\nSplit for 5 agents:")
    for i, (start, end) in enumerate(generator.split_for_agents(5), 1):
        print(f"  Agent {i}: {start} to {end}")
