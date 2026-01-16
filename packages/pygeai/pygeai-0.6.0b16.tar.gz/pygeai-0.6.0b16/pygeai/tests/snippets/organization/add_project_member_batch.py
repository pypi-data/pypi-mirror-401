import csv
from pygeai.organization.clients import OrganizationClient

client = OrganizationClient()

batch_file = "project_members.csv"

successful = 0
failed = 0
errors = []

with open(batch_file, 'r') as f:
    csv_reader = csv.reader(f)
    for line_num, row in enumerate(csv_reader, start=1):
        if len(row) < 3:
            error_msg = f"Line {line_num}: Invalid format - expected at least 3 columns (project_id, email, role1, ...)"
            errors.append(error_msg)
            failed += 1
            continue

        project_id = row[0].strip()
        email = row[1].strip()
        roles = [r.strip() for r in row[2:] if r.strip()]

        if not (project_id and email and roles):
            error_msg = f"Line {line_num}: Missing required fields"
            errors.append(error_msg)
            failed += 1
            continue

        try:
            result = client.add_project_member(project_id, email, roles)
            print(f"Successfully added {email} to project {project_id}")
            successful += 1
        except Exception as e:
            error_msg = f"Line {line_num}: Failed to add {email} to project {project_id}: {str(e)}"
            errors.append(error_msg)
            failed += 1

print(f"\nBatch processing complete: {successful} successful, {failed} failed")
if errors:
    print("\nErrors:")
    for error in errors:
        print(f"  - {error}")
