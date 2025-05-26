#!/usr/bin/env python3
"""
Script to analyze and display the consolidated data gathered by the Data Consolidation Agent
"""
import yaml
import os
from datetime import datetime

def analyze_consolidated_data():
    """Analyze and display the consolidated data"""
    
    data_file = '/home/aistudio/git_source/claude_agent_release_notes/cisco-mds-release-agent/data/output/upgrade_paths.yaml'
    
    if not os.path.exists(data_file):
        print("❌ No consolidated data file found!")
        return
    
    with open(data_file, 'r') as f:
        data = yaml.safe_load(f)
    
    print("🔍 Cisco MDS Release Note Data Analysis")
    print("=" * 50)
    
    # Metadata Analysis
    metadata = data.get('metadata', {})
    print(f"📅 Last Updated: {metadata.get('last_updated_utc', 'Unknown')}")
    print(f"📋 Schema Version: {metadata.get('data_schema_version', 'Unknown')}")
    
    # Source URLs
    source_urls = metadata.get('source_urls', {})
    print(f"🌐 Main Index URL: {source_urls.get('main_index', 'Unknown')}")
    print(f"🌐 Recommended Releases URL: {source_urls.get('recommended_releases', 'Unknown')}")
    
    # Releases Analysis
    releases = data.get('releases', {})
    print(f"\n📦 Total Releases Found: {len(releases)}")
    
    # Group by type
    type_counts = {}
    for version, release_data in releases.items():
        release_type = release_data.get('type', 'Unknown')
        type_counts[release_type] = type_counts.get(release_type, 0) + 1
    
    print("\n📊 Releases by Type:")
    for release_type, count in type_counts.items():
        print(f"   • {release_type}: {count} releases")
    
    # Detailed Release Information
    print("\n📋 Detailed Release Information:")
    for version, release_data in releases.items():
        print(f"\n   🔖 {version} ({release_data.get('type', 'Unknown')})")
        print(f"      Full Version: {release_data.get('full_version_string', 'Unknown')}")
        print(f"      Release Date: {release_data.get('initial_release_date', 'Unknown')}")
        print(f"      Title: {release_data.get('title', 'Unknown')}")
        print(f"      Source: {release_data.get('source_url', 'Unknown')}")
    
    # Recommended Releases
    rec_releases = data.get('recommended_releases', {})
    open_systems = rec_releases.get('open_systems', {})
    ficon = rec_releases.get('ficon', {})
    
    print(f"\n🎯 Recommended Releases:")
    print(f"   • Open Systems: {len(open_systems)} recommendations")
    print(f"   • FICON: {len(ficon)} recommendations")
    
    print("\n✅ Data consolidation analysis complete!")

if __name__ == "__main__":
    analyze_consolidated_data()
