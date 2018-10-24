DROP TABLE IF EXISTS elements;

CREATE TABLE elements(
  id                INTEGER PRIMARY KEY,
  elementName       VARCHAR(50),
  isEnd             INTEGER,
  isIndexed         INTEGER,
  isRoot            INTEGER,
  parentElementId   INTEGER
);

INSERT INTO elements VALUES (0, 'MainElement', 0, 1, 1, -1),
