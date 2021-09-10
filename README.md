# test-gh-actions
Repository to test usage of GH actions

This repository contains code that runs a GH Action as a cron job or on a push. It demonstrates accessing a Google sheet that has a Service Account with access to the sheet, using credentials stored in an encrypted json file that is decrypted based on a GH stored secret. 

The core code that interacts with the spreadsheet via the Google Sheets API and also updates this README with some logging information (the last two lines below) is `test.py`.

Here's a test of the functionality of the Action: 

Number of sheet entries: 4

Last entry processed: 10-09-2021 23:06:54
