SELECT * FROM INFORMATION_SCHEMA.TABLES
order by TABLE_NAME;


-- retrieve the first 20 records from the Theatre Cases table to inspect the data format.
SELECT TOP 20 *
FROM Business_Analyst_Test_Theatre_Cases;

-- retrieve the first 20 records from the Ophthalmology Income table to check for data consistency and format.
SELECT TOP 20 *
FROM NHS_Biz_Ophthalmology_Income;

----------------    Cleaning Business_Analyst_Test_Theatre_Cases    ---------------------------

-- count the number of NULL entries in each column of the Theatre Cases table.
SELECT
    COUNT(*) AS TotalRecords,
    COUNT(CASE WHEN BKCaseNo IS NULL THEN 1 END) AS Null_BKCaseNo,
    COUNT(CASE WHEN CaseType IS NULL THEN 1 END) AS Null_CaseType,
    COUNT(CASE WHEN TreatmentFunction IS NULL THEN 1 END) AS Null_TreatmentFunction,
    COUNT(CASE WHEN ProcedureName IS NULL THEN 1 END) AS Null_ProcedureName
FROM Business_Analyst_Test_Theatre_Cases;




