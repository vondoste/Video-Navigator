<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<body>
<?php
$variable = parse_ini_file("/etc/php/7.4/mods-available/videodb.ini");
$hostname = $variable['db_host'];
$username = $variable['db_user'];
$password = $variable['db_pwd'];
$db = $variable['db_name'];
$dbconnect=mysqli_connect($hostname,$username,$password,$db);
unset($variable);

if ($dbconnect->connect_error) {
	die("Database connection failed: " . $dbconnect->connect_error);
}
?>

<table border="1" align="center">
Rows from the database:
<tr>
	<td>
	URL
	</td>
</tr>
<?php

$query = mysqli_query($dbconnect, "SELECT S.sname, E.season, E.episode, E.ename, E.url FROM episodes AS E, series AS S WHERE S.SeriesID=E.SeriesID")
	or die (mysqli_error($dbconnect));
	
while ($row=mysqli_fetch_array($query)) {
	echo
	"<tr><td><a href=".str_replace(' ','%20',$row['url']).">{$row['url']}</a></td></tr>";
}

?>
</table>

</body>
</html>
