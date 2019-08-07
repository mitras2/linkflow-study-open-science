SELECT SERIAL, QUESTNNR, FB02_01, FB02_02, FB02_03, FB02_04, FB03_01, FB03_02, FB03_03, FB03_04, FB04_01, FB04_02, FB04_03, FB04_04, FB05_01, FB05_02, FB05_03, FB05_04, FB06_01, FB06_02, FB06_03, FB06_04, FB07_01, FB07_02, FB07_03, FB07_04 FROM data_linkedinfo_qnr2
UNION
SELECT SERIAL, QUESTNNR, FR02_01 AS FB02_01, FR02_02 AS FB02_02, FR02_03 AS FB02_03, FR02_04 AS FB02_04, FR03_01 AS FB03_01, FR03_02 AS FB03_02, FR03_03 AS FB03_03, FR03_04 AS FB03_04, FR04_01 AS FB04_01, FR04_02 AS FB04_02, FR04_03 AS FB04_03, FR04_04 AS FB04_04, FR05_01 AS FB05_01, FR05_02 AS FB05_02, FR05_03 AS FB05_03, FR05_04 AS FB05_04, FR06_01 AS FB06_01, FR06_02 AS FB06_02, FR06_03 AS FB06_03, FR06_04 AS FB06_04, FR07_01 AS FB07_01, FR07_02 AS FB07_02, FR07_03 AS FB07_03, FR07_04 AS FB07_04 FROM data_linkedinfo_qnr3
ORDER BY SERIAL, QUESTNNR