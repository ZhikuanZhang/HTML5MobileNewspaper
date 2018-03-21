<html>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<head>
    <title>Test.......</title>
</head>
<body>
<h1>Test---------</h1>
<form>
    <table>
    <tr><td>报纸编号： </td><td><input type="text" name="paperid" size="8"></td></tr>
    <tr><td>印刷日期： </td><td><input type="text" name="date" size="8"></td></tr>
    <tr><td align="center"><input  type="submit" value=" 发送 "></td></tr>
    </table>
</form>

<?php
    $paperid=$_GET["paperid"];
    $date=$_GET["date"];
    if($paperid==null)
        exit;
    header ( "Content-Type: text/html; charset=utf8" );
    $db=new mysqli('127.0.0.1','root','','test');
    $db->query("set character set 'utf8'");//读库
    $db->query("set names 'utf8'");//写库
    $arr=array('00000000000000'=>"------start-----");
    if(mysqli_connect_errno()){
        echo 'Error!!!';
        exit;
    }

    else{

        $query="select id,date,title from news where paperid='".$paperid."' and date='".$date."'";
        echo "<p>".$query."</p>";
        $result=$db->query($query);
        $num_results=$result->num_rows;
        echo"<p>".$date." 共有".$num_results."条新闻，点击标题查看详情</p>";
        for($i=0;$i<$num_results;$i++){
            $row=$result->fetch_assoc();
            $arr[$row['id']]=$row['title'];
        }
        foreach($arr as $key=>$value){
            echo '<br>'.$key.'：'.$value;
        }
        $result->free();
        $db->close();
    }
?>


</body>
</html>
