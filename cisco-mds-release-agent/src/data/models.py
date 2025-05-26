class ReleaseNote:
    def __init__(self, version, initial_release_date, filenames, upgrade_paths, downgrade_paths, resolved_bugs):
        self.version = version
        self.initial_release_date = initial_release_date
        self.filenames = filenames
        self.upgrade_paths = upgrade_paths
        self.downgrade_paths = downgrade_paths
        self.resolved_bugs = resolved_bugs

class EPLDReleaseNote:
    def __init__(self, version, initial_release_date, filenames, disruptive_upgrade, hardware_pmfpga_versions):
        self.version = version
        self.initial_release_date = initial_release_date
        self.filenames = filenames
        self.disruptive_upgrade = disruptive_upgrade
        self.hardware_pmfpga_versions = hardware_pmfpga_versions

class TransceiverFirmwareReleaseNote:
    def __init__(self, version, initial_release_date, filenames, supported_transceivers):
        self.version = version
        self.initial_release_date = initial_release_date
        self.filenames = filenames
        self.supported_transceivers = supported_transceivers

class RecommendedRelease:
    def __init__(self, version, recommended_since, source):
        self.version = version
        self.recommended_since = recommended_since
        self.source = source

class UpgradePath:
    def __init__(self, source_range_description, source_range_logic, steps, notes):
        self.source_range_description = source_range_description
        self.source_range_logic = source_range_logic
        self.steps = steps
        self.notes = notes

class DowngradePath:
    def __init__(self, target_version, steps):
        self.target_version = target_version
        self.steps = steps

class ResolvedBug:
    def __init__(self, bug_id, description):
        self.bug_id = bug_id
        self.description = description