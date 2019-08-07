SELECT "case", qnr, system,
  CASE
    WHEN qnr == 'qnr2' THEN count(*)/21.0
    WHEN qnr == 'qnr3' THEN count(*)/7.0
  END AS 'num_interactions',
  CASE
    WHEN (qnr == 'qnr2' AND system == 'LF') THEN 'LF-qnr2'
    WHEN (qnr == 'qnr2' AND system == 'Folder') THEN 'Folder-qnr2'
    WHEN (qnr == 'qnr3' AND system == 'LF') THEN 'LF-qnr3'
    WHEN (qnr == 'qnr3' AND system == 'Folder') THEN 'Folder-qnr3'
  END AS grouping
FROM interactions WHERE (system != 'setup' AND interaction != 'mouse_scroll_down' AND interaction != 'keyboard_release')
GROUP BY grouping, "case"
ORDER BY "case", timestamp
