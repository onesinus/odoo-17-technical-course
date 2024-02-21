# Install custom module (free custom module example)
Free custom module to do autobackup databases to gcp

https://apps.odoo.com/apps/modules/17.0/backup_to_gcp

# Qweb reports output pdf
Reference: https://www.odoo.com/documentation/17.0/developer/reference/backend/reports.html

After creating pdf output (qweb report) we can access the pdf file directly to the url with this format

<odoo_url>/report/pdf/report/<report_name>/<id_record>

examples

http://localhost:8069/report/pdf/estate.report_estate/1

http://localhost:8069/report/pdf/estate.report_estate/2

it will return pdf file on your browser

# serve api Notes
Reference: https://www.odoo.com/documentation/17.0/developer/reference/backend/http.html

# Submit App Notes

Odoo publish url: https://apps.odoo.com/apps/upload

Example url submitted

ssh://git@github.com/onesinus/odoo-17-technical-course.git#17.0

remember to put version in the end of url 

e.g: #17.0
