<!DOCTYPE html>
<html>
<head>
    <title>Result</title>
</head>
<body>
    <h1>Result</h1>
    <?php
        if (isset($_POST["num1"]) && isset($_POST["num2"])) {
            $num1 = $_POST["num1"];
            $num2 = $_POST["num2"];


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
