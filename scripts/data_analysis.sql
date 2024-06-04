

-------------   calculating the number of cases by Treatment Function and Case Type ---------------
SELECT 
    TreatmentFunction,  
    CaseType,           
    COUNT(*) AS NumberOfCases  
FROM 
    Business_Analyst_Test_Theatre_Cases  
GROUP BY 
    TreatmentFunction, 
    CaseType
ORDER BY 
    TreatmentFunction, 
    CaseType;


--------------  calculating the number of cases by Procedure Name and Case Type  --------------
SELECT 
    ProcedureName,  
    CaseType,       
    COUNT(*) AS NumberOfCases  
FROM 
    Business_Analyst_Test_Theatre_Cases 
GROUP BY 
    ProcedureName, 
    CaseType
ORDER BY 
    ProcedureName, 
    CaseType;


    -------------   finding the top 20 elective procedures by number of cases   --------------
SELECT TOP 20
    ProcedureName,
    COUNT(*) AS NumberOfCases
FROM 
    Business_Analyst_Test_Theatre_Cases
WHERE 
    CaseType = 'Elective'
GROUP BY 
    ProcedureName
ORDER BY 
    NumberOfCases DESC;



-- calculating the average duration of surgery for elective procedures
SELECT 
    ProcedureName,
    AVG(DurationOfSurgeryMinutes) AS AverageDuration  
FROM 
    Business_Analyst_Test_Theatre_Cases
WHERE 
    CaseType = 'Elective' 
GROUP BY 
    ProcedureName
ORDER BY 
    AverageDuration DESC;



-------------   finding the top 10 procedures with the longest average duration ----------------
SELECT TOP 10
    ProcedureName,
    AVG(DurationOfSurgeryMinutes) AS AverageDuration
FROM 
    Business_Analyst_Test_Theatre_Cases
WHERE 
    CaseType = 'Elective'
GROUP BY 
    ProcedureName
ORDER BY 
    AverageDuration DESC;



----------------- finding the top 10 procedures with the shortest average duration  --------------------
SELECT TOP 10
    ProcedureName,
    AVG(DurationOfSurgeryMinutes) AS AverageDuration
FROM 
    Business_Analyst_Test_Theatre_Cases
WHERE 
    CaseType = 'Elective'
GROUP BY 
    ProcedureName
ORDER BY 
    AverageDuration ASC;



    ------- analyze overall patterns of start and finish times for elective Ophthalmology   -------
SELECT
    'Start On Time' AS Event, AVG(StartOnTime) AS AverageOccurrence
FROM Business_Analyst_Test_Theatre_Cases
WHERE CaseType = 'Elective' AND TreatmentFunction = 'Ophthalmology'
UNION ALL
SELECT
    'Early Start' AS Event, AVG(EarlyStart) AS AverageOccurrence
FROM Business_Analyst_Test_Theatre_Cases
WHERE CaseType = 'Elective' AND TreatmentFunction = 'Ophthalmology'
UNION ALL
SELECT
    'Late Start' AS Event, AVG(LateStart) AS AverageOccurrence
FROM Business_Analyst_Test_Theatre_Cases
WHERE CaseType = 'Elective' AND TreatmentFunction = 'Ophthalmology'
UNION ALL
SELECT
    'Finish On Time' AS Event, AVG(FinishedOnTime) AS AverageOccurrence
FROM Business_Analyst_Test_Theatre_Cases
WHERE CaseType = 'Elective' AND TreatmentFunction = 'Ophthalmology'
UNION ALL
SELECT
    'Early Finish' AS Event, AVG(EarlyFinish) AS AverageOccurrence
FROM Business_Analyst_Test_Theatre_Cases
WHERE CaseType = 'Elective' AND TreatmentFunction = 'Ophthalmology'
UNION ALL
SELECT
    'Late Finish' AS Event, AVG(LateFinish) AS AverageOccurrence
FROM Business_Analyst_Test_Theatre_Cases
WHERE CaseType = 'Elective' AND TreatmentFunction = 'Ophthalmology';



-------------   SQL Query to find the top 5 consultants with the most late starts ------------
SELECT TOP 5
    Consultant,
    COUNT(*) AS LateStarts
FROM Business_Analyst_Test_Theatre_Cases
WHERE CaseType = 'Elective' AND TreatmentFunction = 'Ophthalmology' AND LateStart = 1
GROUP BY Consultant
ORDER BY LateStarts DESC;


------  theatres with the most late starts   --------
SELECT TOP 5
    TheatreName,
    COUNT(*) AS LateStarts
FROM Business_Analyst_Test_Theatre_Cases
WHERE CaseType = 'Elective' AND TreatmentFunction = 'Ophthalmology' AND LateStart = 1
GROUP BY TheatreName
ORDER BY LateStarts DESC;

------   the theatre with the most early finishes   ------------
SELECT TOP 10
    TheatreName,
    COUNT(*) AS EarlyFinishes
FROM Business_Analyst_Test_Theatre_Cases
WHERE CaseType = 'Elective' AND TreatmentFunction = 'Ophthalmology' AND EarlyFinish = 1
GROUP BY TheatreName
ORDER BY EarlyFinishes DESC;



------- identify the top 10 most efficient Ophthalmology procedures by shortest average duration
SELECT TOP 10
    ProcedureName,
    AVG(DurationOfSurgeryMinutes) AS AverageDuration
FROM
    Business_Analyst_Test_Theatre_Cases
WHERE
    CaseType = 'Elective' AND TreatmentFunction = 'Ophthalmology'
GROUP BY
    ProcedureName
ORDER BY
    AverageDuration ASC;  -- Ascending order to get the shortest durations at the top



---------   calculate potential income for the top five efficient Ophthalmology procedures -----------
SELECT
    a.ProcedureName,
    b.Income,
    a.AverageDuration
FROM
    (SELECT TOP 10
        ProcedureName,
        AVG(DurationOfSurgeryMinutes) AS AverageDuration
     FROM
        Business_Analyst_Test_Theatre_Cases
     WHERE
        CaseType = 'Elective' AND TreatmentFunction = 'Ophthalmology'
     GROUP BY
        ProcedureName
     ORDER BY
        AverageDuration ASC) a
JOIN
    NHS_Biz_Ophthalmology_Income b ON a.ProcedureName = b.Procedure_Name;


