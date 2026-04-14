DELETE FROM ai_models a USING (
    SELECT path as pat
    FROM ai_models 
    GROUP BY (path) HAVING COUNT(*) > 1
) b
WHERE a.path <> b.pat;

SELECT * FROM ai_models;