CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_addTrans`(IN p_date date,  IN p_description varchar(500), IN p_amt float, IN p_code varchar(50))
BEGIN
	insert into transactions(transDate, description, amt, transCode) values(STR_TO_DATE(p_date, '%d/%m/%Y'), p_description, p_amt, p_code, NOW() );
END