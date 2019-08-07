SELECT QUESTNNR, FB08_01-1, (((FB08_01-1)/6.0)*100.0) as att_scale, count() AS size FROM data_linkedinfo_qnr2
GROUP BY FB08_01
UNION
SELECT QUESTNNR, FB08_01-1, (((FB08_01-1)/6.0)*100.0) as att_scale, count() AS size FROM data_linkedinfo_qnr3
GROUP BY FB08_01
ORDER BY QUESTNNR
