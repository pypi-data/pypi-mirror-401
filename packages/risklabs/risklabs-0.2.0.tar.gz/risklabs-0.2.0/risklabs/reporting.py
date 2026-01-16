import json
from dataclasses import dataclass
from typing import Any
from risklabs.analysis_models import RobustnessMatrix

REPORT_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RiskLab Report</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { background-color: #0f172a; color: #e2e8f0; }
        .card { background-color: #1e293b; border-radius: 0.5rem; padding: 1.5rem; }
        .quadrant { border: 1px solid #334155; height: 100px; display: flex; align-items: center; justify-content: center; flex-direction: column; }
    </style>
</head>
<body class="font-sans antialiased">
    <div class="container mx-auto px-4 py-8">
        <header class="flex justify-between items-center mb-8">
            <div>
                <h1 class="text-3xl font-bold text-blue-400 tracking-tight">
                    RiskLab 
                    <span class="text-gray-500 text-lg font-normal">| Robustness Report</span>
                    <span class="text-xs text-gray-600 block mt-1 font-normal">
                        by <a href="https://eiffellabs.com/" target="_blank" class="hover:text-blue-400 transition-colors">Eiffel Labs</a>
                    </span>
                </h1>
            </div>
            <div class="flex gap-4">
                 <button onclick="toggleModal('docsModal')" class="bg-blue-600 hover:bg-blue-700 text-white font-bold px-4 py-2 rounded text-sm transition transition-colors">
                    ? How to Read
                </button>
                 <div id="decisionBadge" class="bg-gray-700 text-white font-bold px-4 py-2 rounded">
                    DECISION: <span id="decisionText">--</span>
                </div>
                <div id="scoreBadge" class="bg-gray-700 text-gray-300 px-3 py-2 rounded font-mono">
                    Score: <span id="aggScore">--</span>
                </div>
            </div>
        </header>

        <!-- Decision Scorecard -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div class="card md:col-span-2">
                <h2 class="text-xl font-semibold mb-4 text-gray-100">Decision Confidence</h2>
                <div class="flex items-center gap-6">
                    <div class="w-32 text-center">
                        <div class="text-4xl font-bold text-blue-400" id="confRating">--%</div>
                        <div class="text-xs text-gray-500 uppercase tracking-widest mt-1">Confidence</div>
                    </div>
                    <div class="flex-1 border-l border-gray-700 pl-6">
                        <div class="grid grid-cols-2 gap-4 mb-4">
                            <div>
                                <div class="text-sm text-gray-400 mb-1">Tail Amplification Ratio</div>
                                <div class="text-lg font-mono text-gray-200" id="tailRatio">--</div>
                                <div class="text-xs text-gray-500">vs Bench (Lower is better)</div>
                            </div>
                            <div>
                                <div class="text-sm text-gray-400 mb-1">Key Sensitivities</div>
                                <div class="text-sm text-gray-200 font-mono" id="assumptionRank">--</div>
                                <div class="text-xs text-gray-500">Top factors driving risk</div>
                            </div>
                        </div>
                        <div id="freezeTriggers">
                            <!-- Populated by JS -->
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="card">
                <h2 class="text-xl font-semibold mb-4 text-gray-100">Fragility Gauge</h2>
                <div class="text-center py-4">
                     <div class="text-3xl font-bold mb-2" id="fragilityScore">--</div>
                     <div class="w-full bg-gray-700 rounded-full h-2.5 mb-2">
                        <div id="fragilityBar" class="bg-red-500 h-2.5 rounded-full" style="width: 0%"></div>
                     </div>
                     <div class="text-sm text-gray-400">Parameter Sensitivity (0-100)</div>
                </div>
            </div>
        </div>

        <!-- Regime Map -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <div class="card">
                <h2 class="text-xl font-semibold mb-4 text-gray-100">Regime Dependence Map</h2>
                <div class="grid grid-cols-2 gap-2 text-center text-sm">
                    <div class="quadrant bg-gray-800 rounded-tl-lg">
                        <span class="text-gray-500">Bull / Low Vol</span>
                        <span class="text-lg font-bold text-green-400" id="sharpeBL">--</span>
                    </div>
                    <div class="quadrant bg-gray-800 rounded-tr-lg">
                        <span class="text-gray-500">Bull / High Vol</span>
                        <span class="text-lg font-bold text-yellow-400" id="sharpeBH">--</span>
                    </div>
                    <div class="quadrant bg-gray-800 rounded-bl-lg">
                        <span class="text-gray-500">Bear / Low Vol</span>
                        <span class="text-lg font-bold text-red-400" id="sharpeRL">--</span>
                    </div>
                    <div class="quadrant bg-gray-800 rounded-br-lg">
                        <span class="text-gray-500">Bear / High Vol</span>
                        <span class="text-lg font-bold text-red-500" id="sharpeRH">--</span>
                    </div>
                </div>
                <div class="mt-4 text-xs text-center text-gray-500">Sharpe Ratio per Regime</div>
            </div>
            <div class="card h-80">
                <h3 class="text-gray-400 mb-2 font-semibold">Scenario Stress Test</h3>
                <div class="relative h-full w-full p-2">
                    <canvas id="scoreChart"></canvas>
                </div>
            </div>
             <div class="card h-80 md:col-span-2">
                <h3 class="text-gray-400 mb-2 font-semibold">Sensitivity Sweep (Volatility)</h3>
                <div class="relative h-full w-full p-2">
                    <canvas id="sensitivityChart"></canvas>
                </div>
            </div>
        </div>

        <!-- Main Grid -->
        <div class="grid grid-cols-1 gap-6">
            <!-- Robustness Matrix -->
            <div class="card">
                <h2 class="text-xl font-semibold mb-4 text-gray-100">Detailed Scenario Results</h2>
                <div class="overflow-x-auto">
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="text-gray-400 border-b border-gray-700">
                                <th class="py-3">Scenario</th>
                                <th class="py-3">Robustness Score</th>
                                <th class="py-3">Max Drawdown</th>
                                <th class="py-3">Sharpe Ratio</th>
                            </tr>
                        </thead>
                        <tbody id="resultsBody" class="divide-y divide-gray-700">
                            <!-- JS will populate -->
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>

    <!-- Documentation Modal -->
    <div id="docsModal" class="fixed inset-0 bg-black bg-opacity-75 hidden flex items-center justify-center z-50 overflow-y-auto" onclick="if(event.target === this) toggleModal('docsModal')">
        <div class="bg-gray-800 rounded-lg max-w-3xl w-full m-4 p-8 relative shadow-2xl border border-gray-700">
            <button onclick="toggleModal('docsModal')" class="absolute top-4 right-4 text-gray-400 hover:text-gray-200">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
            </button>
            
            <h2 class="text-2xl font-bold text-blue-400 mb-6 border-b border-gray-700 pb-2">Understanding This Report</h2>
            
            <div class="space-y-6 text-gray-300">
                <div>
                    <h3 class="font-bold text-gray-100 text-lg mb-1">Decision Confidence Rating</h3>
                    <p class="text-sm">A composite score (0-100%) indicating how safe it is to approve this strategy. It penalizes for high fragility, tail risk, and regime dependence.</p>
                </div>
                
                <div>
                     <h3 class="font-bold text-gray-100 text-lg mb-1">Regime Dependence Map</h3>
                     <p class="text-sm">Visualizes performance (Sharpe Ratio) across 4 market regimes. Ideally, a strategy should be "All Weather" (positive in all green/red quadrants).</p>
                     <ul class="list-disc list-inside text-xs mt-1 text-gray-400">
                        <li><strong>Bull / Low Vol:</strong> Standard growth environment.</li>
                        <li><strong>Bear / High Vol:</strong> Crash/Crisis environment (Most critical).</li>
                     </ul>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <h3 class="font-bold text-gray-100 text-lg mb-1">Fragility Score</h3>
                        <p class="text-sm">Measures how much performance degrades when assumptions (like weights) are slightly perturbed. High score = High Fragility.</p>
                    </div>
                    <div>
                         <h3 class="font-bold text-gray-100 text-lg mb-1">Tail Amplification</h3>
                         <p class="text-sm">Ratio of the strategy's tail risk (CVaR) to the generic market (SPY). Values > 1.0 mean your downside is <em>worse</em> than the market.</p>
                    </div>
                </div>
                
                <div>
                     <h3 class="font-bold text-gray-100 text-lg mb-1">Assumption Sensitivity</h3>
                     <p class="text-sm">Identifies the primary driver of variance. Helps pinpoint "what matters most" in your model's stability.</p>
                </div>
            </div>
            
            <div class="mt-8 pt-4 border-t border-gray-700 text-right">
                <button onclick="toggleModal('docsModal')" class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded">Close</button>
            </div>
        </div>
    </div>

    <script>
        function toggleModal(id) {
            const el = document.getElementById(id);
            el.classList.toggle('hidden');
        }

        // Data Injection
        const matrix = {{DATA_JSON}};

        document.addEventListener('DOMContentLoaded', () => {
            renderTable(matrix);
            renderChart(matrix);
            renderSensitivity(matrix);
            renderDecision(matrix);
            renderRegimes(matrix);
            
            document.getElementById('aggScore').innerText = matrix.aggregate_score.toFixed(1);
        });

        function renderSensitivity(matrix) {
            if (!matrix.sensitivity_profile || matrix.sensitivity_profile.steps.length === 0) return;
            
            const ctx = document.getElementById('sensitivityChart').getContext('2d');
            const p = matrix.sensitivity_profile;
            
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: p.steps.map(s => s.toFixed(1) + 'x'),
                    datasets: [{
                        label: 'Sharpe Ratio',
                        data: p.sharpes,
                        borderColor: '#60a5fa', // blue-400
                        backgroundColor: 'rgba(96, 165, 250, 0.2)',
                        tension: 0.3,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            grid: { color: '#334155' },
                            ticks: { color: '#94a3b8' },
                            title: { display: true, text: 'Sharpe Ratio', color: '#64748b' }
                        },
                        x: {
                            grid: { color: '#334155' },
                            ticks: { color: '#94a3b8' },
                            title: { display: true, text: p.parameter_name, color: '#64748b' }
                        }
                    },
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                             intersect: false,
                             mode: 'index'
                        }
                    }
                }
            });
        }

        function renderDecision(matrix) {
            const d = matrix.decision_scorecard;
            const f = matrix.fragility_matrix;
            
            // Confidence
            document.getElementById('confRating').innerText = d.confidence_rating.toFixed(0) + '%';
            document.getElementById('tailRatio').innerText = d.tail_amplification_ratio.toFixed(2) + 'x';

            // Assumptions
            if(d.assumption_sensitivity_rank && d.assumption_sensitivity_rank.length > 0) {
                 const content = d.assumption_sensitivity_rank.slice(0, 2).map(x => `<span class="bg-gray-800 px-1 rounded">${x}</span>`).join(' ');
                 document.getElementById('assumptionRank').innerHTML = content;
            } else {
                 document.getElementById('assumptionRank').innerText = 'None Detected';
            }
            
            // Decision Badge
            const badge = document.getElementById('decisionBadge');
            const text = document.getElementById('decisionText');
            text.innerText = d.recommendation;
            
            if(d.recommendation === 'APPROVE') badge.classList.add('bg-green-600');
            else if(d.recommendation === 'REJECT') badge.classList.add('bg-red-600');
            else badge.classList.add('bg-yellow-600');
            
            // Triggers
            const trigDiv = document.getElementById('freezeTriggers');
            if(d.freeze_triggers && d.freeze_triggers.length > 0) {
                 d.freeze_triggers.forEach(t => {
                     const el = document.createElement('div');
                     el.className = 'text-red-400 text-sm font-semibold flex items-center gap-2';
                     el.innerHTML = '<span>⚠️</span> ' + t;
                     trigDiv.appendChild(el);
                 });
            } else {
                trigDiv.innerHTML = '<div class="text-green-400 text-sm">No Freeze Triggers Detected</div>';
            }
            
            // Fragility
            document.getElementById('fragilityScore').innerText = f.fragility_score.toFixed(1);
            document.getElementById('fragilityBar').style.width = f.fragility_score + '%';
        }

        function renderRegimes(matrix) {
            const r = matrix.regime_profile;
            document.getElementById('sharpeBL').innerText = r.sharpe_bull.toFixed(2);
            document.getElementById('sharpeBH').innerText = r.sharpe_high_vol.toFixed(2);
            document.getElementById('sharpeRL').innerText = r.sharpe_low_vol.toFixed(2); // Using low vol as proxy for bear low? Mapped loosely for now
            document.getElementById('sharpeRH').innerText = r.sharpe_bear.toFixed(2);
        }

        function renderTable(matrix) {
            const tbody = document.getElementById('resultsBody');
            tbody.innerHTML = '';
            
            matrix.scenario_results.forEach(res => {
                const tr = document.createElement('tr');
                const scoreColor = res.robustness_score < 30 ? 'text-red-400' : 'text-green-400';
                
                tr.innerHTML = `
                    <td class="py-3 font-medium text-gray-200">${res.scenario_name}</td>
                    <td class="py-3 ${scoreColor} font-bold">${res.robustness_score.toFixed(1)}</td>
                    <td class="py-3 text-red-300">${(res.max_drawdown * 100).toFixed(1)}%</td>
                    <td class="py-3 text-blue-300">${res.sharpe_ratio.toFixed(2)}</td>
                `;
                tbody.appendChild(tr);
            });
        }

        function renderChart(matrix) {
            const ctx = document.getElementById('scoreChart').getContext('2d');
            const labels = matrix.scenario_results.map(r => r.scenario_name);
            const data = matrix.scenario_results.map(r => r.robustness_score);
            const colors = data.map(v => v < 30 ? 'rgba(239, 68, 68, 0.7)' : 'rgba(34, 197, 94, 0.7)');

            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Robustness Score',
                        data: data,
                        backgroundColor: colors,
                        borderColor: colors.map(c => c.replace('0.7', '1')),
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100,
                            grid: { color: '#334155' },
                            ticks: { color: '#94a3b8' }
                        },
                        x: {
                            grid: { display: false },
                            ticks: { color: '#94a3b8' }
                        }
                    },
                    plugins: {
                        legend: { display: false }
                    }
                }
            });
        }
    </script>
</body>
</html>
"""

class RiskReport:
    def __init__(self, matrix: RobustnessMatrix):
        self.matrix = matrix

    def to_file(self, filename: str) -> None:
        """
        Generates the HTML report and writes it to the specified file.
        """
        # Convert Pydantic model to dict, then JSON
        json_data = json.dumps(self.matrix.model_dump(mode='json'))
        
        # Inject into template
        html_content = REPORT_TEMPLATE.replace("{{DATA_JSON}}", json_data)
        
        with open(filename, 'w') as f:
            f.write(html_content)
        
        print(f"Report saved to {filename}")
