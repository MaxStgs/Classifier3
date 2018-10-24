delete from test;
insert into test values (0, 'E1', -1), (1, 'E2', 0), (2, 'E3', 0), (3, 'E4', 0), (4, 'E3', 1), (5, 'E4', 1);

insert into test values (6, 'E5', 5);

WITH RECURSIVE b(parentElementId,id,elementName,isEnd,isIndexed,isRoot) AS
(
    SELECT 6,0,0,0,0,0
    UNION ALL
    SELECT elements.parentElementId, elements.id,
           elements.elementName, elements.isEnd,
           elements.isIndexed, elements.isRoot
    FROM b, elements
    WHERE b.parentElementId = elements.id
               limit 10
) SELECT * FROM b;

WITH RECURSIVE b(x,w) AS
(
    SELECT 6, 0
    UNION ALL
    SELECT elements.parentElementId,elements.id
    FROM b, elements
    WHERE b.x = elements.id
               limit 10
) SELECT * FROM b;