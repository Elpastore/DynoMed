document.addEventListener('DOMContentLoaded', function() {
    // Profile picture preview
    const profilePictureInput = document.getElementById('profile-picture');
    const profilePicturePreview = document.getElementById('profile-picture-preview');
    const profilePicturePlaceholder = document.getElementById('profile-picture-placeholder');
    const profilePictureContainer = document.getElementById('profile-picture-container');

    profilePictureInput.addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                profilePicturePreview.src = e.target.result;
                profilePicturePreview.style.display = 'block';
                profilePicturePlaceholder.style.display = 'none';
                profilePictureContainer.style.backgroundColor = 'transparent';
            }
            reader.readAsDataURL(file);
        } else {
            profilePicturePreview.style.display = 'none';
            profilePicturePlaceholder.style.display = 'block';
            profilePictureContainer.style.backgroundColor = '#f8f9fa';  // Light gray background
        }
    });

    // University and Degree fields
    let universityDegreeCount = 1;
    const universityContainer = document.getElementById('university-degree-container');
    const addUniversityButton = document.getElementById('add-university-degree');

    addUniversityButton.addEventListener('click', function() {
        const newFields = document.createElement('div');
        newFields.className = 'row g-3 mb-3';
        newFields.innerHTML = `
            <div class="col-md-3">
                <label for="education-country-${universityDegreeCount}" class="form-label">Country of Education</label>
                <select class="form-select" id="education-country-${universityDegreeCount}" name="education-country-${universityDegreeCount}" required>
                    <option value="">Choose...</option>
                    <option value="US">United States</option>
                    <option value="UK">United Kingdom</option>
                    <option value="CA">Canada</option>
                    <!-- Add more countries as needed -->
                </select>
            </div>
            <div class="col-md-3">
                <label for="professional_data-education-university-${universityDegreeCount}" class="form-label">University</label>
                <input type="text" class="form-control" id="professional_data-education-university-${universityDegreeCount}" name="professional_data-education-university-${universityDegreeCount}" list="university-list-${universityDegreeCount}" required>
                <datalist id="university-list-${universityDegreeCount}">
                    <option value="Harvard University">
                    <option value="Oxford University">
                    <option value="Stanford University">
                    <!-- Add more universities as needed -->
                </datalist>
            </div>
            <div class="col-md-4">
                <label for="professional_data-education-degree-${universityDegreeCount}" class="form-label">Degree</label>
                <input type="text" class="form-control" id="professional_data-education-degree-${universityDegreeCount}" name="professional_data-education-degree-${universityDegreeCount}" required>
            </div>
            <div class="col-md-2 d-flex align-items-end">
                <button type="button" class="btn btn-danger remove-university-degree">Remove</button>
            </div>
        `;
        universityContainer.appendChild(newFields);
        universityDegreeCount++;
    });

    // Event delegation for remove university/degree buttons
    universityContainer.addEventListener('click', function(e) {
        if (e.target && e.target.classList.contains('remove-university-degree')) {
            e.target.closest('.row').remove();
        }
    });

    // Certificate fields
    let certificateCount = 1;
    const certificateContainer = document.getElementById('certificate-container');
    const addCertificateButton = document.getElementById('add-certificate');

    addCertificateButton.addEventListener('click', function() {
        const newFields = document.createElement('div');
        newFields.className = 'row g-3 mb-3';
        newFields.innerHTML = `
            <div class="col-md-4">
                <label for="certificate-type-${certificateCount}" class="form-label">Certificate Type</label>
                <select class="form-select" id="certificate-type-${certificateCount}" name="certificate-type-${certificateCount}" required>
                    <option value="">Choose...</option>
                    <option value="degree">Degree Certificate</option>
                    <option value="professional">Professional Certificate</option>
                    <option value="training">Training Certificate</option>
                    <option value="other">Other</option>
                </select>
            </div>
            <div class="col-md-6">
                <label for="certificate-file-${certificateCount}" class="form-label">Upload Certificate</label>
                <input type="file" class="form-control" id="certificate-file-${certificateCount}" name="certificate-file-${certificateCount}" accept=".pdf,.jpg,.jpeg,.png" required>
            </div>
            <div class="col-md-2 d-flex align-items-end">
                <button type="button" class="btn btn-danger remove-certificate">Remove</button>
            </div>
        `;
        certificateContainer.appendChild(newFields);
        certificateCount++;
    });

    // Event delegation for remove certificate buttons
    certificateContainer.addEventListener('click', function(e) {
        if (e.target && e.target.classList.contains('remove-certificate')) {
            e.target.closest('.row').remove();
        }
    });
});