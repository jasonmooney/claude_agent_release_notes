import re
import yaml
from datetime import datetime
from typing import Dict, List, Any, Optional

class AIQueryAssistant:
    def __init__(self, data_source=None):
        self.data_source = data_source
        self.data = self._load_data()

    def query_upgrade_path(self, current_version: str, target_version: str, platform: str = "open_systems") -> Dict[str, Any]:
        """Query upgrade path between two versions for a specific platform."""
        try:
            current_version = self._normalize_version(current_version)
            target_version = self._normalize_version(target_version)
            
            if current_version not in self.data.get('releases', {}):
                return {
                    'status': 'error',
                    'message': f"Current version {current_version} not found in database",
                    'available_versions': list(self.data.get('releases', {}).keys())
                }
            
            current_release = self.data['releases'][current_version]
            upgrade_paths = current_release.get('upgrade_paths_from_this_version', {}).get(platform, [])
            
            # Check if direct upgrade path exists
            direct_path = None
            for path in upgrade_paths:
                if target_version in path.get('target_version', ''):
                    direct_path = path
                    break
            
            if direct_path:
                return {
                    'status': 'success',
                    'upgrade_type': 'direct',
                    'from_version': current_version,
                    'to_version': target_version,
                    'platform': platform,
                    'path': direct_path,
                    'resolved_bugs': self.data['releases'].get(target_version, {}).get('resolved_bugs', [])
                }
            else:
                # Look for multi-hop paths (future enhancement)
                return {
                    'status': 'not_found',
                    'message': f"No direct upgrade path found from {current_version} to {target_version}",
                    'available_upgrades': upgrade_paths,
                    'suggestion': "Consider upgrading to an intermediate version first"
                }
        except Exception as e:
            return {'status': 'error', 'message': f"Error querying upgrade path: {str(e)}"}

    def query_downgrade_path(self, current_version: str, target_version: str, platform: str = "open_systems") -> Dict[str, Any]:
        """Query downgrade path between two versions for a specific platform."""
        try:
            current_version = self._normalize_version(current_version)
            target_version = self._normalize_version(target_version)
            
            if current_version not in self.data.get('releases', {}):
                return {
                    'status': 'error',
                    'message': f"Current version {current_version} not found in database"
                }
            
            current_release = self.data['releases'][current_version]
            downgrade_paths = current_release.get('downgrade_paths_from_this_version', {}).get(platform, [])
            
            # Check if direct downgrade path exists
            direct_path = None
            for path in downgrade_paths:
                if target_version in path.get('target_version', ''):
                    direct_path = path
                    break
            
            if direct_path:
                return {
                    'status': 'success',
                    'downgrade_type': 'direct',
                    'from_version': current_version,
                    'to_version': target_version,
                    'platform': platform,
                    'path': direct_path
                }
            else:
                return {
                    'status': 'not_found',
                    'message': f"No direct downgrade path found from {current_version} to {target_version}",
                    'available_downgrades': downgrade_paths
                }
        except Exception as e:
            return {'status': 'error', 'message': f"Error querying downgrade path: {str(e)}"}

    def query_recommended_release(self, platform: str = "open_systems") -> Dict[str, Any]:
        """Query recommended release for a specific platform."""
        try:
            recommended = self.data.get('recommended_releases', {}).get(platform, {})
            
            if recommended:
                return {
                    'status': 'success',
                    'platform': platform,
                    'recommended_release': recommended,
                    'last_updated': self.data.get('metadata', {}).get('last_updated_utc')
                }
            else:
                # If no specific recommendation, suggest latest stable release
                releases = self.data.get('releases', {})
                latest_version = max(releases.keys()) if releases else None
                
                return {
                    'status': 'partial',
                    'message': f"No specific recommendation found for {platform}",
                    'suggested_latest': latest_version,
                    'note': "Consider the latest stable release or consult Cisco documentation"
                }
        except Exception as e:
            return {'status': 'error', 'message': f"Error querying recommended release: {str(e)}"}

    def query_resolved_bugs(self, version: str) -> Dict[str, Any]:
        """Query resolved bugs for a specific version."""
        try:
            version = self._normalize_version(version)
            
            if version not in self.data.get('releases', {}):
                return {
                    'status': 'error',
                    'message': f"Version {version} not found in database",
                    'available_versions': list(self.data.get('releases', {}).keys())
                }
            
            release = self.data['releases'][version]
            resolved_bugs = release.get('resolved_bugs', [])
            
            return {
                'status': 'success',
                'version': version,
                'release_date': release.get('initial_release_date'),
                'total_bugs_resolved': len(resolved_bugs),
                'resolved_bugs': resolved_bugs,
                'upgrade_paths_available': len(release.get('upgrade_paths_from_this_version', {}).get('open_systems', []))
            }
        except Exception as e:
            return {'status': 'error', 'message': f"Error querying resolved bugs: {str(e)}"}

    def query_release_date(self, version: str) -> Dict[str, Any]:
        """Query the release date for a specific version."""
        try:
            version = self._normalize_version(version)
            
            if version not in self.data.get('releases', {}):
                return {
                    'status': 'error',
                    'message': f"Version {version} not found in database",
                    'available_versions': list(self.data.get('releases', {}).keys())
                }
            
            release = self.data['releases'][version]
            release_date = release.get('initial_release_date')
            
            return {
                'status': 'success',
                'version': version,
                'full_version_string': release.get('full_version_string'),
                'release_date': release_date,
                'bugs_resolved': len(release.get('resolved_bugs', []))
            }
        except Exception as e:
            return {'status': 'error', 'message': f"Error querying release date: {str(e)}"}

    def natural_language_query(self, query: str) -> Dict[str, Any]:
        """Process natural language queries and route to appropriate methods."""
        query_lower = query.lower()
        
        # Extract version numbers from query
        version_pattern = r'(\d+\.\d+(?:\.\d+)?(?:[a-z])?)'
        versions = re.findall(version_pattern, query)
        
        try:
            # Upgrade path queries
            if any(word in query_lower for word in ['upgrade', 'update', 'path to']):
                if len(versions) >= 2:
                    platform = 'ficon' if 'ficon' in query_lower else 'open_systems'
                    return self.query_upgrade_path(versions[0], versions[1], platform)
                elif len(versions) == 1:
                    return {'status': 'clarification_needed', 'message': 'Please specify target version for upgrade'}
                else:
                    return {'status': 'clarification_needed', 'message': 'Please specify current and target versions'}
            
            # Downgrade queries
            elif any(word in query_lower for word in ['downgrade', 'rollback']):
                if len(versions) >= 2:
                    platform = 'ficon' if 'ficon' in query_lower else 'open_systems'
                    return self.query_downgrade_path(versions[0], versions[1], platform)
                else:
                    return {'status': 'clarification_needed', 'message': 'Please specify current and target versions for downgrade'}
            
            # Bug queries
            elif any(word in query_lower for word in ['bug', 'fix', 'issue', 'csc']):
                if versions:
                    return self.query_resolved_bugs(versions[0])
                else:
                    return {'status': 'clarification_needed', 'message': 'Please specify a version to check for resolved bugs'}
            
            # Release date queries
            elif any(word in query_lower for word in ['date', 'when', 'released']):
                if versions:
                    return self.query_release_date(versions[0])
                else:
                    return {'status': 'clarification_needed', 'message': 'Please specify a version to check release date'}
            
            # Recommended release queries
            elif any(word in query_lower for word in ['recommend', 'suggest', 'best', 'latest']):
                platform = 'ficon' if 'ficon' in query_lower else 'open_systems'
                return self.query_recommended_release(platform)
            
            # General help
            else:
                return {
                    'status': 'help',
                    'message': 'I can help with Cisco MDS release information. Try asking:',
                    'examples': [
                        'What bugs were fixed in version 9.4.3?',
                        'How do I upgrade from 9.2.2 to 9.4.3?',
                        'What is the recommended release for open systems?',
                        'When was version 9.4.3a released?'
                    ],
                    'available_versions': list(self.data.get('releases', {}).keys())
                }
        except Exception as e:
            return {'status': 'error', 'message': f"Error processing query: {str(e)}"}

    def start_interactive_session(self):
        """Start an interactive query session."""
        print("🤖 Cisco MDS AI Query Assistant")
        print("=" * 50)
        print("Ask me anything about Cisco MDS release notes!")
        print("Type 'quit' or 'exit' to end the session.\n")
        
        while True:
            try:
                user_input = input("❓ Your question: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Thank you for using the Cisco MDS AI Query Assistant!")
                    break
                
                if not user_input:
                    continue
                
                print("🔍 Processing your query...")
                response = self.natural_language_query(user_input)
                self._display_response(response)
                print()
                
            except KeyboardInterrupt:
                print("\n👋 Thank you for using the Cisco MDS AI Query Assistant!")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")

    def _display_response(self, response: Dict[str, Any]):
        """Display formatted response to user."""
        status = response.get('status', 'unknown')
        
        if status == 'success':
            if 'upgrade_type' in response:
                print(f"✅ Upgrade Path Found:")
                print(f"   From: {response['from_version']}")
                print(f"   To: {response['to_version']}")
                print(f"   Platform: {response['platform']}")
                if response.get('resolved_bugs'):
                    print(f"   Bugs resolved in target version: {len(response['resolved_bugs'])}")
            elif 'version' in response and 'resolved_bugs' in response:
                print(f"🐛 Resolved Bugs in {response['version']}:")
                print(f"   Release Date: {response.get('release_date', 'Unknown')}")
                print(f"   Total Bugs Resolved: {response['total_bugs_resolved']}")
                for bug in response['resolved_bugs'][:5]:  # Show first 5 bugs
                    print(f"   • {bug.get('id', 'Unknown')}: {bug.get('description', 'No description')}")
                if len(response['resolved_bugs']) > 5:
                    print(f"   ... and {len(response['resolved_bugs']) - 5} more bugs")
            elif 'release_date' in response:
                print(f"📅 Release Information:")
                print(f"   Version: {response['version']}")
                print(f"   Release Date: {response['release_date']}")
                print(f"   Bugs Resolved: {response.get('bugs_resolved', 0)}")
            else:
                print(f"✅ {response.get('message', 'Query successful')}")
        
        elif status == 'error':
            print(f"❌ Error: {response.get('message', 'Unknown error')}")
        
        elif status == 'not_found':
            print(f"⚠️  {response.get('message', 'Information not found')}")
            if response.get('suggestion'):
                print(f"💡 Suggestion: {response['suggestion']}")
        
        elif status == 'clarification_needed':
            print(f"❓ {response.get('message', 'Please provide more information')}")
        
        elif status == 'help':
            print(f"ℹ️  {response.get('message', 'Help information')}")
            if response.get('examples'):
                print("   Examples:")
                for example in response['examples']:
                    print(f"   • {example}")

    def _load_data(self) -> Dict[str, Any]:
        """Load data from YAML file or data source."""
        try:
            if self.data_source:
                return self.data_source
            
            # Try to load from default file location
            yaml_file = "/home/aistudio/git_source/claude_agent_release_notes/cisco-mds-release-agent/data/output/upgrade_paths.yaml"
            with open(yaml_file, 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            print(f"Warning: Could not load data: {str(e)}")
            return {'releases': {}, 'recommended_releases': {}, 'metadata': {}}

    def _normalize_version(self, version: str) -> str:
        """Normalize version string to match data format."""
        # Remove common prefixes and normalize format
        version = version.replace('v', '').replace('V', '')
        
        # Convert format like 9.4(3) to 9.4.3
        version = re.sub(r'(\d+\.\d+)\((\d+[a-z]?)\)', r'\1.\2', version)
        
        return version

    def combined_query(self, current_version: str, target_version: str, platform: str = "open_systems") -> Dict[str, Any]:
        """Handle combined queries for upgrade paths and comprehensive information."""
        upgrade_result = self.query_upgrade_path(current_version, target_version, platform)
        bug_result = self.query_resolved_bugs(target_version)
        
        return {
            'upgrade_path': upgrade_result,
            'target_version_bugs': bug_result,
            'combined_analysis': {
                'upgrade_available': upgrade_result.get('status') == 'success',
                'bugs_fixed_in_target': bug_result.get('total_bugs_resolved', 0),
                'recommendation': 'Upgrade recommended' if upgrade_result.get('status') == 'success' else 'Check upgrade path'
            }
        }