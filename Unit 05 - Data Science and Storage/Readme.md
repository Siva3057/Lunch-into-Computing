Reflection: 

SQL vs NoSQL for this dataset

This dataset is small (323 annual and 3,871 monthly rows) and strictly tabular: every record has the same three fields, and each is uniquely identified by source plus date. That favours a relational database such as PostgreSQL or SQLite. A composite primary key on (source, date) would reject duplicates at ingestion instead of leaving me to check for them in pandas, and a separate sources table could store each agency's baseline, the one inconsistency I had to correct by hand. The analysis was relational as well: decade means are a GROUP BY, the trend is a regression over an ordered series, and comparing GISTEMP with GCAG is a join on year.

A NoSQL document store would add little here. Its strengths are flexible schemas and horizontal scaling, which matter when records vary in shape or arrive at huge volume, such as station-level readings with differing metadata or gridded satellite data. If the project grew that way, a document or time-series store could absorb heterogeneous records more easily, though I would lose joins and strict constraints.

For this use case, SQL is the better fit: fixed schema, small volume, aggregation-heavy analysis. Local storage is sufficient; the cloud would matter only for sharing or scale.
