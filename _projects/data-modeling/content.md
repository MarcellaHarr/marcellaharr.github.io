## Overview

This was the second project in the Advanced Data Wrangling and Data Modeling course, and it followed directly after Real World Data Wrangling. Where that first project focused on gathering and cleaning data from scratch, this one flipped the focus to organizing already-collected data into a proper relational database.

The assignment came from Udacity, using a fictional music streaming company called Sparkify as the scenario. Sparkify's analytics team wanted to understand what songs users were listening to, but their data was sitting in raw JSON log files and song metadata files instead of a queryable database. My job was to build a Postgres database using a star schema, then write a Python ETL pipeline to extract data from the JSON files, transform it into the right shape, and load it into that database.

The star schema itself was part of the assignment's requirements rather than something I designed from scratch. It called for one fact table, songplays, to record each individual song play event, and four dimension tables, users, songs, artists, and time, to hold the supporting details around each play. I still had to work out the specific columns, data types, and relationships myself, but the overall shape of the schema was dictated by the project.

The hardest part of the whole project was writing the song_select query that connects a song play log entry back to the right song and artist. The log files don't include a song ID or artist ID directly, so I had to query the songs and artists tables using the song title, artist name, and duration from the log to find a match. Since the log data only covers a small sample of user activity while the song data covers a much larger, separate catalog, most log entries wouldn't find a matching song in the songs table, so the query was written to handle that gracefully and insert a NULL songid and artistid whenever no match was found.

## Designing the Star Schema

The database follows a star schema, with one fact table at the center and four supporting dimension tables around it. The songplays table is the fact table, and it records every individual song play event pulled from the log files. The four dimension tables, users, songs, artists, and time, hold the descriptive details that give each song play its context.

- songplays: songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
- users: user_id, first_name, last_name, gender, level
- songs: song_id, title, artist_id, year, duration
- artists: artist_id, name, location, latitude, longitude
- time: start_time, hour, day, week, month, year, weekday

This structure was set by the project itself rather than something I chose on my own. Udacity's rubric specifically called for a fact table and four dimension tables in this exact configuration. Working within that structure still meant deciding on the actual column types, primary keys, and constraints myself, and it made clear why a star schema fits this kind of data in the first place. Splitting user, song, artist, and time details out into their own tables means none of that information has to repeat on every single songplay row, and it keeps each table focused on one kind of information instead of mixing them together.

For the NOT NULL constraints, I applied them wherever the rubric allowed it, mainly on the primary keys and on the fields that the log data always provides, like user_id and start_time. I left songid and artistid in the songplays table nullable, since the song_select query often can't find a match between a log entry and the songs table, and forcing NOT NULL there would have broken the insert step every time that happened.

create_tables.py drops and recreates all five tables at the start of every run, which kept the schema clean each time I tested changes to the ETL pipeline without worrying about leftover data from a previous run.

## Building the ETL Pipeline

Before I touched the etl.py script file, I built and tested every step in the etl.ipynb notebook, working through one song file and one log file at a time until each piece worked the way it was supposed to. Once something worked in the notebook, I moved it over into the script file as its own function.

Song data and log data ended up going through the same basic process. Read the JSON file into a dataframe, pull out and reshape the columns each table needed, then insert. The song file logic was fairly direct, since each file only holds one song and one artist. The log file logic did more work up front, filtering down to just the NextSong events and converting the timestamp before it could build out the time, users, and songplays records, including the song_select lookup for matching a log entry back to its songid and artistid.

What actually let the script file run across the whole dataset, instead of just the one file I tested in the notebook, was a function that walks through a folder, finds every JSON file in it, and then loops over that list running whichever processing step it was handed. It also commits after every file and prints a running count of how many files it had gotten through, which mattered more than I expected. Watching "12 of 30 files processed" scroll by was the difference between knowing the pipeline was working and just hoping it hadn't silently stalled somewhere in the middle.

I also had to think through what should happen when the same record showed up more than once across different files. For songs, artists, and time, I just skipped the insert if that record already existed, since none of that data changes once it's created. Users were different. A user's subscription level can flip from free to paid or back again between log files, so instead of skipping the insert, I updated the existing row with whatever level showed up most recently. That felt like the more accurate approach, since I wanted the users table to reflect where someone's account actually stood, not just what it looked like the first time they showed up in the logs.

Every function in the script file also got a docstring explaining what it does and what it takes in, which the rubric called for directly as part of code quality. It was a small thing, but it made the script easier to read back later.

## Conclusion

By the end of this project, I'd built both halves of what a working database needs, a schema that made sense for the data and a pipeline that could actually fill it. Designing the star schema forced me to think about table structure, keys, and constraints on their own, before any ETL logic came into play. Then building the pipeline meant handling the messier reality of the data itself, log entries that didn't match a song, users whose subscription level changed mid-stream, and records that could show up more than once across different files. Both halves mattered about equally. A well-designed schema doesn't help much if the pipeline loading it can't handle real data, and a solid pipeline doesn't mean much without a schema that organizes what it's loading.

Once the tables were built and the pipeline had run, I used the test.ipynb notebook Udacity provided to run through the sanity tests, checking that every table had actually been created and that records had landed where they should. That verification step gave me confidence the whole pipeline worked end to end, not just that individual pieces ran without errors.

As the second project in the Advanced Data Wrangling and Data Modeling course, this one felt like a natural next step after Real World Data Wrangling. That first project was about gathering and cleaning data from scratch, and this one picked up from there, taking already-collected data and giving it a proper home in a relational database built for the kind of questions Sparkify's analytics team would actually want to ask.
