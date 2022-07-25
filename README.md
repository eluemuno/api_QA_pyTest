# api_QA_pyTest

This is an implementation of an API testing framework using pytest. The basic flow is to extract an API response on requiremensts per country using randomly generating ISO-3 country codes from a pre-populated list. The country codes are included as part of the payload for the POST. THe response is stored as a json. 

At this early stage I have extracted the description and using regexp checked for special characters (which is something that has come up a few times). If there are no special characters the test returns None.

The next implementation will be to compare certain aspects with the source db.
