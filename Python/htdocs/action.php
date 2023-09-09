<!DOCTYPE html>
<html>
<head>
    <title>Result</title>
</head>
<body>
    <h1>Result</h1>
    <?php
        if (isset($_GET["num1"]) && isset($_GET["num2"])) {
            $num1 = $_GET["num1"];
            $num2 = $_GET["num2"];


            if (!is_numeric($num1) || !is_numeric($num2)) {
                echo "Please enter valid numbers.";
            } else {
                $sum = $num1 + $num2;
                echo "The sum of $num1 and $num2 is: $sum";
            }
        }
    ?>
</body>
</html>
