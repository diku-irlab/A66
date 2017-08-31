The Project
===========
This dataset was developed at the department of Computer Science at the University of Copenhagen (DIKU) in connection with the following article:

_Evaluation Measures for Relevance and Credibility in Ranked Lists_  
Christina Lioma, Jakob Grue Simonsen, and Birger Larsen (2017)  
ACM SIGIR International Conference on the Theory of Information Retrieval, _In press_.

[download from arXiv](https://arxiv.org/abs/1708.07157)


The Data
========
The file `data` is a comma seperated values file with the following format:

    pid, qid, rank, url_id, rel, cred, comments

Below is a brief description of the columns.

      COLUMN   VALUE RANGE   DESCRIPTION
         pid   [1,10]        unique identifier for each participants
         qid   [1,10]        unique identifier for each query
        rank   [1,5]         rank of each query result
      url_id   [101,225]     unique identifier for each url
         rel   [1,4]         relevance score
        cred   [1,4]         credibility score
    comments                 some users provided comments for their scores,
                             otherwise the token <NA> is present

The file `urls` is a file that maps `url_id`'s to their corresponding plaintext representation


The Task
========
For each of the 10 queries listed below, please do the following:
1. Submit the query to Google
2. Click on each of the top 5 results for that query, read it, and assign separately:
   - a score of relevance of that result  to the query (using the scale specified below)
   - a score of credibility of that result (using the scale specified below)

How relevant the clicked webpage is to the query should not affect your assessment of its credibility (relevance and credibility are unrelated). Please use your own understanding of relevance and credibility.

If you do not understand the query, or if you are unsure about the credibility of the webpage, you can open a separate browser and try to gather more information on the topic of the query.

Queries
-------
1. Smoking not bad for health
2. Princess Diana alive
3. Trump scientologist
4. UFO sightings
5. Loch Ness monster sightings
6. Vaccines bad for children
7. Time travel proof
8. Brexit illuminati
9. Climate change not dangerous
10. Digital tv surveillance

Relevance scale
---------------
1. Not relevant at all
2. Marginally relevant
3. Medium relevant
4. Completely relevant

Credibility scale
-----------------
1. Not credible at all
2. Marginally credible
3. Medium credible
4. Completely credible
