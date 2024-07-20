<script>
    document.addEventListener('DOMContentLoaded', function() {
        let universityDegreeCount = 1;
        const container = document.getElementById('university-degree-container');
        const addButton = document.getElementById('add-university-degree');

        addButton.addEventListener('click', function() {
            const newFields = document.createElement('div');
            newFields.className = 'row g-3 mb-3';
            newFields.innerHTML = `
                <div class="col-md-6">
                    <label for="professional_data-education-university-${universityDegreeCount}" class="form-label">University</label>
                    <input type="text" class="form-control" id="professional_data-education-university-${universityDegreeCount}" name="professional_data-education-university-${universityDegreeCount}">
                </div>
                <div class="col-md-6">
                    <label for="professional_data-education-degree-${universityDegreeCount}" class="form-label">Degree</label>
                    <input type="text" class="form-control" id="professional_data-education-degree-${universityDegreeCount}" name="professional_data-education-degree-${universityDegreeCount}">
                </div>
            `;
            container.appendChild(newFields);
            universityDegreeCount++;
        });
    });
</script>