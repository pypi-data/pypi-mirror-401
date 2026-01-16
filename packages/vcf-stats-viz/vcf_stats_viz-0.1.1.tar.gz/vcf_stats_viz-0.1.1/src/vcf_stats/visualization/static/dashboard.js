let currentPage = 1;
    let perPage = 50;
    let totalPages = 1;
    let currentData = {};
    let chromosomeChart = null;
    let variantTypeChart = null;

    document.addEventListener('DOMContentLoaded', function() {
        loadAvailableAnalyses();
    });

    async function loadAvailableAnalyses() {
        try {
            const response = await fetch('/api/files');

            if (!response.ok) {
                throw new Error(`HTTP Error: ${response.status}`);
            }

            const data = await response.json();
            const selector = document.getElementById('analysisSelector');

            if (data.analyses && data.analyses.length > 0) {
                selector.innerHTML = '<option value="">Select an analysis...</option>';

                data.analyses.forEach(analysis => {
                    const option = document.createElement('option');
                    option.value = analysis.id;
                    option.textContent = `${analysis.name} (${analysis.total_variants.toLocaleString()} variants)`;
                    selector.appendChild(option);
                });

                selector.value = data.analyses[0].id;
                loadAnalysis(data.analyses[0].id);

            } else {
                selector.innerHTML = '<option value="">No analyses available</option>';
                showError('No analyses found in results directory.');
            }

            selector.onchange = function() {
                if (this.value) {
                    loadAnalysis(this.value);
                }
            };

        } catch (error) {
            console.error('Error loading analyses:', error);
            showError('Error loading analyses: ' + error.message);
        }
    }

    async function loadAnalysis(analysisId) {
        showLoading();

        try {
            const response = await fetch(`/api/load/${analysisId}`);

            if (!response.ok) {
                throw new Error(`HTTP Error: ${response.status}`);
            }

            const result = await response.json();

            if (result.status === 'success') {
                await loadAllData();
            } else {
                throw new Error(result.error || 'Unknown error');
            }
        } catch (error) {
            console.error('Error:', error);
            showError('Error loading analysis: ' + error.message);
        } finally {
            hideLoading();
        }
    }

    async function loadAllData() {
        try {
            const summaryResponse = await fetch('/api/data/summary');
            if (!summaryResponse.ok) throw new Error('Error loading summary');
            currentData.summary = await summaryResponse.json();

            const chartsResponse = await fetch('/api/data/charts');
            if (!chartsResponse.ok) throw new Error('Error loading charts');
            currentData.charts = await chartsResponse.json();

            const metadataResponse = await fetch('/api/data/metadata');
            if (metadataResponse.ok) {
                currentData.metadata = await metadataResponse.json();
            }

            updateMainStats();
            createCharts();
            loadVariantsTable();

            showSuccess('Data loaded successfully!');

        } catch (error) {
            console.error('Error loading data:', error);
            showError('Error loading data: ' + error.message);
        }
    }

    function updateMainStats() {
        if (currentData.summary) {
            document.getElementById('totalVariants').textContent = 
                currentData.summary.total_variants?.toLocaleString() || '0';
            document.getElementById('chromosomesCount').textContent = 
                Object.keys(currentData.summary.chromosome_counts || {}).length;
            document.getElementById('variantTypesCount').textContent = 
                Object.keys(currentData.summary.variant_type_counts || {}).length;
            document.getElementById('memoryUsage').textContent = 
                (currentData.summary.memory_usage_mb || 0) + ' MB';

            document.getElementById('mainStats').style.display = 'flex';
        }
    }

    function createCharts() {
        if (!currentData.charts) {
            return;
        }

        const chromCtx = document.getElementById('chromosomeChart').getContext('2d');

        if (chromosomeChart) {
            chromosomeChart.destroy();
        }

        if (currentData.charts.chromosome_distribution) {
            const chromData = currentData.charts.chromosome_distribution;

            chromosomeChart = new Chart(chromCtx, {
                type: 'bar',
                data: {
                    labels: chromData.labels || [],
                    datasets: [{
                        label: 'Number of Variants',
                        data: chromData.values || [],
                        backgroundColor: 'rgba(54, 162, 235, 0.8)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: false
                        },
                        title: {
                            display: true,
                            text: 'Chromosome Distribution'
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Number of Variants'
                            }
                        },
                        x: {
                            title: {
                                display: true,
                                text: 'Chromosome'
                            }
                        }
                    }
                }
            });
        } else {
            document.getElementById('chromosomeChart').innerHTML = '<p class="text-muted">No data available</p>';
        }

        const variantCtx = document.getElementById('variantTypeChart').getContext('2d');

        if (variantTypeChart) {
            variantTypeChart.destroy();
        }

        if (currentData.charts.variant_types) {
            const variantData = currentData.charts.variant_types;

            variantTypeChart = new Chart(variantCtx, {
                type: 'pie',
                data: {
                    labels: variantData.labels || [],
                    datasets: [{
                        data: variantData.values || [],
                        backgroundColor: [
                            '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0',
                            '#9966FF', '#FF9F40', '#8AC926', '#C9CBCF',
                            '#1982C4', '#6A4C93', '#F15BB5', '#00BBF9'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'right'
                        },
                        title: {
                            display: true,
                            text: 'Variant Types'
                        }
                    }
                }
            });
        } else {
            document.getElementById('variantTypeChart').innerHTML = '<p class="text-muted">No data available</p>';
        }
    }

    async function loadVariantsTable(page = 1) {
        try {
            showLoading();
            const response = await fetch(`/api/data/variants?page=${page}&per_page=${perPage}`);
            const data = await response.json();

            if (data.error) {
                const tbody = document.getElementById('variantsTable');
                tbody.innerHTML = `
                    <tr>
                        <td colspan="7" class="text-center text-muted">
                            <i class="fas fa-info-circle me-2"></i>
                            ${data.note || 'Data not available in streaming mode'}
                        </td>
                    </tr>
                `;
                document.getElementById('paginationInfo').textContent = 
                    `Streaming mode: ${data.total_variants_estimated?.toLocaleString() || '0'} estimated variants`;
                return;
            }

            if (data.variants) {
                const tbody = document.getElementById('variantsTable');
                tbody.innerHTML = '';

                data.variants.forEach(variant => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${variant.CHROM}</td>
                        <td>${variant.POS.toLocaleString()}</td>
                        <td>${variant.ID || '-'}</td>
                        <td>${variant.REF}</td>
                        <td>${variant.ALT}</td>
                        <td>${getGeneDisplay(variant)}</td>
                        <td><span class="badge bg-secondary">${variant.VARIANT_TYPE}</span></td>
                    `;
                    tbody.appendChild(row);
                });

                currentPage = data.page;

                if (data.is_sample) {
                    document.getElementById('paginationInfo').textContent = 
                        `Sample: ${data.sample_size?.toLocaleString() || '0'} of ${data.total_variants_estimated?.toLocaleString() || '0'} variants`;
                    document.getElementById('prevPage').disabled = true;
                    document.getElementById('nextPage').disabled = true;
                } else {
                    totalPages = data.total_pages;
                    updatePaginationInfo();
                }
            }
        } catch (error) {
            console.error('Error loading variants:', error);
            showError('Error loading variant table: ' + error.message);
        } finally {
            hideLoading();
        }
    }

    function getGeneDisplay(variant) {
        const gene = variant.GENE || variant.gene || variant.Gene || 
                    variant.GENE_NAME || variant.gene_name || variant.Gene_Name ||
                    '-';

        if (gene === '-' || !gene) {
            return '<span class="text-muted">-</span>';
        }

        if (Array.isArray(gene)) {
            return gene[0] || '-';
        }

        if (typeof gene === 'string' && gene.length > 30) {
            return `<span title="${gene}">${gene.substring(0, 30)}...</span>`;
        }

        return gene;
    }

    function changePage(direction) {
        const newPage = currentPage + direction;
        if (newPage >= 1 && newPage <= totalPages) {
            loadVariantsTable(newPage);
        }
    }

    function updatePaginationInfo() {
        document.getElementById('paginationInfo').textContent = 
            `Page ${currentPage} of ${totalPages} (${perPage} variants per page)`;

        document.getElementById('prevPage').disabled = currentPage === 1;
        document.getElementById('nextPage').disabled = currentPage === totalPages;
    }

    async function searchVariants() {
        const query = document.getElementById('searchInput').value.trim();
        if (!query) {
            loadVariantsTable(1);
            return;
        }

        try {
            showLoading();
            const response = await fetch(`/api/data/search?q=${encodeURIComponent(query)}`);
            const data = await response.json();

            if (data.results) {
                const tbody = document.getElementById('variantsTable');
                tbody.innerHTML = '';

                if (data.total_found === 0) {
                    tbody.innerHTML = '<tr><td colspan="7" class="text-center text-muted">No results found</td></tr>';
                } else {
                    data.results.forEach(variant => {
                        const row = document.createElement('tr');
                        row.innerHTML = `
                            <td>${variant.CHROM}</td>
                            <td>${variant.POS.toLocaleString()}</td>
                            <td>${variant.ID || '-'}</td>
                            <td>${variant.REF}</td>
                            <td>${variant.ALT}</td>
                            <td>${getGeneDisplay(variant)}</td>
                            <td><span class="badge bg-secondary">${variant.VARIANT_TYPE}</span></td>
                        `;
                        tbody.appendChild(row);
                    });
                }

                document.getElementById('paginationInfo').textContent = 
                    `${data.total_found} results for "${query}"`;

                document.getElementById('prevPage').disabled = true;
                document.getElementById('nextPage').disabled = true;
            }
        } catch (error) {
            console.error('Search error:', error);
            showError('Search error: ' + error.message);
        } finally {
            hideLoading();
        }
    }

    function showLoading() {
        document.getElementById('loading').style.display = 'block';
    }

    function hideLoading() {
        document.getElementById('loading').style.display = 'none';
    }

    function showError(message) {
        let errorDiv = document.getElementById('errorMessage');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.id = 'errorMessage';
            errorDiv.className = 'alert alert-danger alert-dismissible fade show';
            errorDiv.innerHTML = `
                <strong>Error!</strong> <span id="errorText">${message}</span>
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            document.querySelector('.container').prepend(errorDiv);
        } else {
            document.getElementById('errorText').textContent = message;
            errorDiv.style.display = 'block';
        }
    }

    function showSuccess(message) {
        let successDiv = document.getElementById('successMessage');
        if (!successDiv) {
            successDiv = document.createElement('div');
            successDiv.id = 'successMessage';
            successDiv.className = 'alert alert-success alert-dismissible fade show';
            successDiv.innerHTML = `
                <strong>Success!</strong> <span id="successText">${message}</span>
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            document.querySelector('.container').prepend(successDiv);
        } else {
            document.getElementById('successText').textContent = message;
            successDiv.style.display = 'block';
        }
    }

    document.getElementById('searchInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchVariants();
        }
    });

    document.getElementById('searchInput').addEventListener('input', function(e) {
        if (this.value.trim() === '') {
            loadVariantsTable(1);
        }
    });