<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Server Dashboard</title>
    <style>
        body {
            font-family: Arial, sans-serif;
        }
        header {
            background-color: #333;
            color: #fff;
            padding: 20px;
            text-align: center;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .section {
            margin-bottom: 20px;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            background-color: #f9f9f9;
        }

        .dropdown {
            cursor: pointer;
        }

        .dropdown-btn {
            background: none;
            border: none;
            cursor: pointer;
            font-size: 20px;
        }

        .expanded-content {
            display: none;
            padding: 10px;
            background-color: #f9f9f9;
            border-top: 1px solid #ccc;
        }

        .show {
            display: block;
            animation: expandDropdown 0.3s;
        }

        @keyframes expandDropdown {
            from {
                max-height: 0;
                opacity: 0;
            }
            to {
                max-height: 100px;
                opacity: 1;
            }
        }

        .span-p {
            font-size: 24px;
            font-weight: 500;
            color: #333;
            margin-top: 20px;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <header>
        <h1>Server Dashboard</h1>
    </header>
    <div class="container">
        <section class="section">
            <h2>Server Information</h2>
            <?php
            echo "<p>Server Name: Python Web Server</p>";
            echo "<p>Server IP: 127.0.0.1:2728</p>";
            echo "<p>Owner : K.D.T. Srikantha | 21001901 | 2021/CS/190</p>";
            echo "<p>Version : 1.0.0</p>";
            ?>
        </section>
        <section class="section">
            <h2>Server Status</h2>
            <?php
            $server_status = "Online";
            echo "<p>Status: <span style='color: rgb(0, 200, 0);'>" . $server_status . "</span></p>";
            ?>
        </section>

        <section class="section">
            <h2>Server Actions</h2>
            <form method="post">
                <button type="submit" name="shutdown">Shutdown Server</button>
            </form>
        </section>

        <section class="section" id="serverGuideSection">
            <div class="dropdown" onclick="toggleDropdown()">
                <button class="dropdown-btn"><span class="span-p">Instructions</span>▼</button>
            </div>
            <div class="expanded-content" id="expandedContent">
                <!-- Content to show/hide -->
                <p>Here is some information about the server guide.</p>
                <p style="font-size:15px;">This is a simple web server for serve to the php files. Currently it can only serve for the php. The server can handle both GET and POST requests. Also it can identify the <b>index.html</b> and it can identify css and js file differently and add the styles for your website.</p>
            </div>
        </section>

        <section class="section">
            <h2>Contact</h2>
            <p>If you facing any issue, <a href="mailto:dasun.thathsara.sri@gmail.com">contact me</a></p>
        </section>
    </div>
    <script>
        function toggleDropdown() {
            var expandedContent = document.getElementById("expandedContent");
            var serverGuideSection = document.getElementById("serverGuideSection");

            if (expandedContent.style.display === "block") {
                expandedContent.style.display = "none";
                serverGuideSection.style.height = "auto"; // Reset the section height
            } else {
                expandedContent.style.display = "block";
                serverGuideSection.style.height = serverGuideSection.scrollHeight + "px"; // Expand the section
            }
        }
    </script>
</body>
</html>
