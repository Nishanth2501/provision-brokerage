"""
Simple script to seed seminars - Run this once to populate the database
"""

import sys
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from utils.seed_seminars import create_sample_seminars, init_db

if __name__ == "__main__":
    print("🌱 Seeding database with sample seminars...")
    print("=" * 60)
    
    # Initialize database
    init_db()
    
    # Create seminars
    create_sample_seminars()
    
    print("=" * 60)
    print("✅ Done! Refresh your frontend to see the seminars.")

