import os
from datetime import datetime

class HTMLReporter:
    """
    Generates a modern, professional, and responsive HTML report for network scan results.
    This class uses Tailwind CSS for styling and includes a dark mode toggle.
    """
    def __init__(self):
        """Initializes the reporter and ensures the 'reports' directory exists."""
        os.makedirs("reports", exist_ok=True)

    def generate(self, results, log_file=None):
        """
        Generates the HTML report from the scan results.

        Args:
            results (list): A list of dictionaries, where each dictionary represents a scanned device.
            log_file (str, optional): The path to the log file to be linked in the report. Defaults to None.

        Returns:
            str: The filename of the generated report.
        """
        scan_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        filename = f"reports/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"

        # --- Calculate Summary Statistics ---
        total_devices = len(results)
        reachable = [r for r in results if r["status"] == "Reachable"]
        unreachable = [r for r in results if r["status"] == "Unreachable"]
        
        num_reachable = len(reachable)
        num_unreachable = len(unreachable)

        # Calculate average latency, avoiding division by zero
        avg_latency = (
            round(sum(r["latency"] for r in reachable if r.get("latency") is not None) / num_reachable, 2)
            if num_reachable > 0 else 0
        )
        
        # Calculate reachability percentage for the progress bar
        reachability_percent = (num_reachable / total_devices * 100) if total_devices > 0 else 0

        # Create a link for the log file if it exists
        log_link_html = f"<a href='../{log_file}' target='_blank' class='text-indigo-500 dark:text-indigo-400 hover:underline'>View Log File</a>" if log_file else "<span class='text-gray-500 dark:text-gray-400'>Not Available</span>"

        # --- Build the HTML String ---
        html_content = f"""
<!DOCTYPE html>
<html lang="en" class="">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Network Scan Report</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <script>
        // Set dark mode class on page load to prevent FOUC (Flash of Unstyled Content)
        if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {{
            document.documentElement.classList.add('dark');
        }} else {{
            document.documentElement.classList.remove('dark');
        }}
    </script>
    <script>
        tailwind.config = {{
          darkMode: 'class',
          theme: {{
            extend: {{
              fontFamily: {{
                sans: ['Inter', 'sans-serif'],
              }},
            }}
          }}
        }}
    </script>
    <style>
        /* Using a style tag for font-family to ensure it loads reliably */
        body {{
            font-family: 'Inter', sans-serif;
        }}
        /* Simple animation for cards */
        .summary-card {{
            transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
        }}
        .summary-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        }}
        .dark .summary-card:hover {{
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -2px rgba(0, 0, 0, 0.2);
        }}
    </style>
</head>
<body class="bg-gray-100 dark:bg-gray-900 text-gray-800 dark:text-gray-200">

    <div class="container mx-auto p-4 sm:p-6 lg:p-8">

        <!-- Header -->
        <header class="mb-8">
            <div class="flex justify-between items-center">
                <h1 class="text-3xl font-bold text-gray-900 dark:text-white">📡 H+F Skynet© Network Scan Report</h1>
                <button id="theme-toggle" type="button" class="text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-700 rounded-lg text-sm p-2.5">
                    <svg id="theme-toggle-dark-icon" class="hidden w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"></path></svg>
                    <svg id="theme-toggle-light-icon" class="hidden w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" fill-rule="evenodd" clip-rule="evenodd"></path></svg>
                </button>
            </div>
            <p class="text-gray-600 dark:text-gray-400 mt-1">Generated on: {scan_time}</p>
        </header>

        <!-- Summary Dashboard -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <!-- Total Devices Card -->
            <div class="summary-card bg-white dark:bg-gray-800 p-6 rounded-xl shadow-md flex items-center space-x-4">
                <div class="bg-blue-100 dark:bg-blue-900/50 p-3 rounded-full">
                    <svg class="w-6 h-6 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"></path></svg>
                </div>
                <div>
                    <p class="text-sm font-medium text-gray-500 dark:text-gray-400">Total Devices</p>
                    <p class="text-2xl font-bold text-gray-900 dark:text-white">{total_devices}</p>
                </div>
            </div>
            <!-- Reachable Card -->
            <div class="summary-card bg-white dark:bg-gray-800 p-6 rounded-xl shadow-md flex items-center space-x-4">
                <div class="bg-green-100 dark:bg-green-900/50 p-3 rounded-full">
                    <svg class="w-6 h-6 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                </div>
                <div>
                    <p class="text-sm font-medium text-gray-500 dark:text-gray-400">Reachable</p>
                    <p class="text-2xl font-bold text-gray-900 dark:text-white">{num_reachable}</p>
                </div>
            </div>
            <!-- Unreachable Card -->
            <div class="summary-card bg-white dark:bg-gray-800 p-6 rounded-xl shadow-md flex items-center space-x-4">
                <div class="bg-red-100 dark:bg-red-900/50 p-3 rounded-full">
                     <svg class="w-6 h-6 text-red-600 dark:text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                </div>
                <div>
                    <p class="text-sm font-medium text-gray-500 dark:text-gray-400">Unreachable</p>
                    <p class="text-2xl font-bold text-gray-900 dark:text-white">{num_unreachable}</p>
                </div>
            </div>
            <!-- Avg Latency Card -->
            <div class="summary-card bg-white dark:bg-gray-800 p-6 rounded-xl shadow-md flex items-center space-x-4">
                <div class="bg-yellow-100 dark:bg-yellow-900/50 p-3 rounded-full">
                    <svg class="w-6 h-6 text-yellow-600 dark:text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                </div>
                <div>
                    <p class="text-sm font-medium text-gray-500 dark:text-gray-400">Avg. Latency</p>
                    <p class="text-2xl font-bold text-gray-900 dark:text-white">{avg_latency} ms</p>
                </div>
            </div>
        </div>
        
        <!-- Reachability Progress Bar and Log Link -->
        <div class="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-md mb-8">
             <div class="flex justify-between items-center mb-2">
                <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-100">Device Reachability</h3>
                <p class="text-sm font-medium text-gray-600">{log_link_html}</p>
             </div>
            <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-4">
                <div class="bg-green-500 dark:bg-green-600 h-4 rounded-full" style="width: {reachability_percent}%"></div>
            </div>
            <p class="text-right text-sm text-gray-500 dark:text-gray-400 mt-1">{round(reachability_percent, 1)}% Reachable</p>
        </div>

        <!-- Results Table -->
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-md overflow-x-auto">
            <table class="min-w-full">
                <thead class="bg-gray-50 dark:bg-gray-700/50">
                    <tr>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">#</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">IP Address</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">MAC Address</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">MAC Vendor</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Hostname</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Status</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Latency (ms)</th>
                        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Open Ports</th>
                    </tr>
                </thead>
                <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
        """

        # --- Generate Table Rows Dynamically ---
        if not results:
            html_content += """
                    <tr>
                        <td colspan="8" class="px-6 py-12 text-center text-gray-500 dark:text-gray-400">
                            No devices found in the scan.
                        </td>
                    </tr>
            """
        else:
            for idx, device in enumerate(results, start=1):
                # Determine status badge styling
                if device["status"] == "Reachable":
                    status_badge = '<span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300">Reachable</span>'
                else:
                    status_badge = '<span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300">Unreachable</span>'

                # Determine latency styling
                latency_val = device.get('latency')
                if latency_val is None:
                    latency_display = "<span class='text-gray-400 dark:text-gray-500'>N/A</span>"
                elif latency_val > 200:
                    latency_display = f"<span class='font-semibold text-yellow-600 dark:text-yellow-400'>{latency_val}</span>"
                else:
                    latency_display = f"<span class='text-gray-700 dark:text-gray-300'>{latency_val}</span>"

                # Format open ports
                open_ports = ", ".join(map(str, device.get("open_ports", []))) if device.get("open_ports") else "<span class='text-gray-400 dark:text-gray-500'>None</span>"
                
                # Sanitize and get device details with fallbacks
                ip_addr = device.get('ip', 'Unknown')
                mac_addr = device.get('mac', 'Unknown')
                vendor = device.get('vendor', 'Unknown')
                hostname = device.get('hostname', 'Unknown')

                html_content += f"""
                    <tr class="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors duration-150">
                        <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-500 dark:text-gray-400">{idx}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm font-semibold text-gray-900 dark:text-white">{ip_addr}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-300">{mac_addr}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-300">{vendor}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-300">{hostname}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm">{status_badge}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm">{latency_display}</td>
                        <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-300">{open_ports}</td>
                    </tr>
                """

        # --- Footer and Closing Tags ---
        html_content += """
                </tbody>
            </table>
        </div>

        <!-- Footer -->
        <footer class="text-center mt-8">
            <p class="text-sm text-gray-500 dark:text-gray-400">
                Generated by Skynet © 2025 Hein+Fricke. All Rights Reserved.
            </p>
        </footer>

    </div>

    <script>
        // Theme toggle script
        const themeToggleBtn = document.getElementById('theme-toggle');
        const themeToggleDarkIcon = document.getElementById('theme-toggle-dark-icon');
        const themeToggleLightIcon = document.getElementById('theme-toggle-light-icon');

        // Function to set the theme and icon state
        function setTheme() {{
            if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {{
                themeToggleLightIcon.classList.remove('hidden');
                themeToggleDarkIcon.classList.add('hidden');
                document.documentElement.classList.add('dark');
            }} else {{
                themeToggleDarkIcon.classList.remove('hidden');
                themeToggleLightIcon.classList.add('hidden');
                document.documentElement.classList.remove('dark');
            }}
        }}

        // Set initial theme on load
        setTheme();

        themeToggleBtn.addEventListener('click', function() {{
            // Toggle theme
            const isDark = document.documentElement.classList.toggle('dark');
            
            // Update local storage
            localStorage.setItem('color-theme', isDark ? 'dark' : 'light');

            // Update icon visibility
            themeToggleDarkIcon.classList.toggle('hidden');
            themeToggleLightIcon.classList.toggle('hidden');
        }});
    </script>
</body>
</html>
        """

        # --- Write to File ---
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(html_content)
            print(f"Successfully generated report: {filename}")
        except IOError as e:
            print(f"Error writing report file: {e}")
            return None
            
        return filename