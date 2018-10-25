POST_TYPES = [
    'Events',
    'Meeting Notes',
    'News'
]

MEETING_TYPES = [
    ('', ''),
    ('Division', 'Division'),
    ('Strategic Planning', 'Strategic Planning'),
    ('Senior Staff', 'Senior Staff'),
    ('Project', 'Project'),
    ('Agency', 'Agency')
]

DIVISIONS = [
    ('', ''),
    ('Administration & Human Resources', 'Administration & Human Resources'),
    ('Executive', 'Executive'),
    ('External Affairs', 'External Affairs'),
    ('Grants Unit', 'Grants Unit'),
    ('Information Technology', 'Information Technology'),
    ('Legal', 'Legal'),
    ('Municipal Archives', 'Municipal Archives'),
    ('Municipal Library', 'Municipal Library'),
    ('Municipal Records Management', 'Municipal Records Management'),
    ('Operations', 'Operations')
]

# Key is the division name to be used in the URL, '-' in place of spaces
# Value is a dictionary containing the division's HTML template name and plain text name for querying the database
DIVISION_PAGES = {
    'administration-and-human-resources': {
        'template_name': 'administration_and_human_resources',
        'plain_text': 'Administration & Human Resources'
    },
    'executive': {
        'template_name': 'executive',
        'plain_text': 'Executive'
    },
    'external-affairs': {
        'template_name': 'external_affairs',
        'plain_text': 'External Affairs'
    },
    'grant-unit': {
        'template_name': 'grant_unit',
        'plain_text': 'Grant Unit'
    },
    'information-technology': {
        'template_name': 'information_technology',
        'plain_text': 'Information Technology'
    },
    'legal': {
        'template_name': 'legal',
        'plain_text': 'Legal'
    },
    'municipal-archives': {
        'template_name': 'municipal_archives',
        'plain_text': 'Municipal Archives'
    },
    'municipal-library': {
        'template_name': 'municipal_library',
        'plain_text': 'Municipal Library'
    },
    'municipal-records-management': {
        'template_name': 'municipal_records_management',
        'plain_text': 'Municipal Records Management'
    },
    'operations': {
        'template_name': 'operations',
        'plain_text': 'Operations'
    }
}

STAFF_DIRECTORY_FILTERS = [
    ('First Name', 'First Name'),
    ('Last Name', 'Last Name'),
    ('Division', 'Division'),
    ('Title', 'Title')

]

CERT_TYPE = [
    ('', ''),
    ('Birth', 'Birth'),
    ('Death', 'Death'),
    ('Marriage', 'Marriage'),
    ('Marriage License', 'Marriage License')
]

BOROUGHS = [
    ('Manhattan', 'Manhattan'),
    ('Bronx', 'Bronx'),
    ('Brooklyn', 'Brooklyn'),
    ('Queens', 'Queens'),
    ('Richmond', 'Richmond')
]

TAGS = [
    'ACS',
    'Admin',
    'Administration',
    'Aging',
    'Applications',
    'Archives',
    'Archivist',
    'Art',
    'Audit',
    'Benefit',
    'Blog',
    'Book ',
    'Book Signing',
    'Borough President',
    'Bronx',
    'Brooklyn',
    'Budget',
    'Buildings',
    'Bush Terminal',
    'Cable',
    'Calendar',
    'Catalog',
    'Charter',
    'City Clerk',
    'City Council',
    'City Hall',
    'City Planning',
    'Civil',
    'Class',
    'Club',
    'COIB',
    'Commission',
    'Commissioner',
    'Committee',
    'Community',
    'Conservation',
    'Consultant',
    'Coop',
    'Counsel',
    'Cultural affairs',
    'DA',
    'DCAS',
    'DCLA',
    'DCP',
    'DEP',
    'Development',
    'Digital',
    'Digitization',
    'Disability',
    'Disaster',
    'Disposal',
    'Diversity',
    'DOE',
    'DOHMH',
    'DoITT',
    'DOT',
    'DSNY',
    'DYCD',
    'Education',
    'EEO',
    'Elections',
    'Emergency',
    'Event',
    'Executive',
    'Exhibit',
    'External affairs',
    'Facebook',
    'Facilities',
    'Film',
    'Finance',
    'Fire',
    'Fiscal',
    'Gallery',
    'Genealogy',
    'Grants',
    'Group',
    'Guidelines',
    'Hard Copy Reduction',
    'Health',
    'Help Desk',
    'Hours',
    'Housing',
    'HPD',
    'HR',
    'HRA',
    'Human Resources',
    'Industry City',
    'Infrastructure',
    'Initiative',
    'Instagram',
    'Integration',
    'Intern',
    'Internet',
    'Interview',
    'Intranet',
    'IT',
    'Job',
    'Law',
    'Lecture',
    'Librarian',
    'Library',
    'Luna',
    'Manager',
    'Manhattan',
    'Mayor',
    'Media',
    'Meeting',
    'Meeting Notice',
    'Metrics',
    'Microfilm',
    'Migration',
    'MMR',
    'MOCS',
    'Modernization',
    'MRC',
    'MRMD',
    'Network',
    'News',
    'Newsletter',
    'Notice',
    'Notification',
    'NYCERS',
    'NYPD',
    'OLR',
    'OMB',
    'Openrecords',
    'Operations',
    'Outreach',
    'Panel',
    'Paper Conversion',
    'Paper Reduction',
    'Permission',
    'Personnel',
    'Photo',
    'Photography',
    'Pick Up',
    'Police ',
    'Policy',
    'Portal',
    'Preservation',
    'Procedure',
    'Procurement',
    'Program',
    'Publication',
    'Purchases',
    'Purchasing',
    'Qualifications',
    'Queens',
    'QWL',
    'Reading Room',
    'Recognition',
    'Records',
    'Records Management',
    'Reference',
    'Report',
    'Research',
    'Rules',
    'Safety',
    'Sanitation',
    'SBS',
    'Screening',
    'Senior Staff',
    'Signs',
    'Staten Island',
    'Student',
    'Support',
    'Survey',
    'SYEP',
    'Test',
    'Timesheet',
    'Tour',
    'Training',
    'Tumblr',
    'Twitter',
    'Union',
    'Upgrade',
    'Veteran\'s Affairs',
    'Warehouse',
    'Website',
    'Wifi',
    'Women\'s Activism',
    'YouTube'
]

DOCUMENT_TYPES = [
    ('', ''),
    ('Instructions', 'Instructions'),
    ('Policies and Procedures', 'Policies and Procedures'),
    ('Templates', 'Templates'),
    ('Training Materials', 'Training Materials')
]