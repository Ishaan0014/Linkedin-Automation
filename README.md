LinkedIn Automation

#Project Overview
Networking is crucial for business professionals, but manually searching for
connections and sending requests on LinkedIn is time-consuming. This project
automates LinkedIn searches and connection requests, helping users expand
their professional network efficiently

#Objectives

1.Automate LinkedIn profile searches based on specific job roles (e.g.,"Business Analyst").

2.Send connection requests automatically while maintaining LinkedIn’s security guidelines.

3.Log processed profiles to avoid duplicate requests.

	
#Tools & Technologies Used

1.Python & Selenium WebDriver – For automating LinkedIn searches and
connection requests.

2.LinkedIn Search Filters – Used to refine job title and location-based
searches.

3.Data Logging (CSV/Excel) – To store requested connections and track
progress.


#Implementation Process
1. User Input: The script takes input for job title (e.g., "Data Scientist") and
location (e.g., "London").
2. Automating Search: Selenium automates LinkedIn’s search bar to find
matching profiles.
3. Sending Connection Requests: The script iterates through profiles,
clicking "Connect" on each profile while avoiding spam-like behavior.
4. Logging Connections: Successfully sent requests are stored in an Excel
file, preventing duplicate requests
