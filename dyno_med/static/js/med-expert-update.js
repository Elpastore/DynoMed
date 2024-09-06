// Function to add more education fields
function addEducation() {
    let educationCount = $('.form-section[id^="education"]').length + 1;
    $('#educationContainer').append(`
        <div class="form-section" id="education${educationCount}">
            <h5>Education ${educationCount}</h5>
            <div class="mb-3">
                <label for="university${educationCount}" class="form-label">University</label>
                <input type="text" class="form-control" id="university${educationCount}" name="university[]" placeholder="University Name" required>
            </div>
            <div class="mb-3">
                <label for="course${educationCount}" class="form-label">Course</label>
                <input type="text" class="form-control" id="course${educationCount}" name="course[]" placeholder="Course Name" required>
            </div>
            <div class="mb-3">
                <label for="entryYear${educationCount}" class="form-label">Year of Entry</label>
                <input type="month" class="form-control" id="entryYear${educationCount}" name="entryYear[]" min="1980-01" max="2024-12" required>
            </div>
            <div class="mb-3">
                <label for="endYear${educationCount}" class="form-label">Year of Completion</label>
                <input type="month" class="form-control" id="endYear${educationCount}" name="endYear[]" min="1980-01" max="2024-12" required>
            </div>
            <div class="mb-3">
                <label for="degree${educationCount}" class="form-label">Degree</label>
                <select class="form-control" id="degree${educationCount}" name="degree[]" required>
                    <option value="" disabled selected>Select Degree</option>
                    <option value="Bachelor of Medicine, Bachelor of Surgery (MBBS)">Bachelor of Medicine, Bachelor of Surgery (MBBS)</option>
                    <option value="Doctor of Medicine (MD)">Doctor of Medicine (MD)</option>
                    <option value="Bachelor of Science in Nursing (BSN)">Bachelor of Science in Nursing (BSN)</option>
                    <option value="Master of Science in Nursing (MSN)">Master of Science in Nursing (MSN)</option>
                    <option value="Diploma in Nursing">Diploma in Nursing</option>
                    <option value="PhD in Medicine">PhD in Medicine</option>
                    <option value="Master of Surgery (MS)">Master of Surgery (MS)</option>
                </select>
            </div>
            <button type="button" class="btn btn-danger remove-education" data-id="${educationCount}">Remove</button>
        </div>
    `);
}

// Function to add more certification fields
function addCertification() {
    let certificationCount = $('.form-section[id^="certification"]').length + 1;
    $('#certificationContainer').append(`
        <div class="form-section" id="certification${certificationCount}">
            <h5>Certification ${certificationCount}</h5>
            <div class="mb-3">
                <label for="certificationName${certificationCount}" class="form-label">Certification Name</label>
                <input type="text" class="form-control" id="certificationName${certificationCount}" name="certificationName[]" placeholder="Certification Name" required>
            </div>
            <div class="mb-3">
                <label for="certificationFile${certificationCount}" class="form-label">Upload Certificate</label>
                <input type="file" class="form-control" id="certificationFile${certificationCount}" name="certificationFile[]" accept=".pdf,.jpg,.png" required>
            </div>
            <button type="button" class="btn btn-danger remove-certification" data-id="${certificationCount}">Remove</button>
        </div>
    `);
}

$(document).ready(function() {
    // Add more education details

    // Initialize datepicker for date of birth
    $('#datepicker').datepicker({
        format: 'yyyy-mm-dd',
        autoclose: true,
        todayHighlight: true,
        endDate: new Date(),  // Restricts selection to dates up to today
        yearRange: '1900:' + new Date().getFullYear()  // Allows selection from year 1900 to current year
    });

    $('#addEducation').click(addEducation);

    // Remove education entry
    $(document).on('click', '.remove-education', function() {
        let id = $(this).data('id');
        $('#education' + id).remove();
    });

    // Add more certifications
    $('#addCertification').click(addCertification);

    // Remove a specific certification section
    $(document).on('click', '.remove-certification', function() {
        let id = $(this).data('id');
        $('#certification' + id).remove();
    });
});
