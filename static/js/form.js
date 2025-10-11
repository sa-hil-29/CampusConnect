// CampusConnect Forms JS - Dynamic Form Features
document.addEventListener('DOMContentLoaded', function() {
    try {
        // Real-time eligibility preview for job creation
        const eligibilityField = document.getElementById('id_eligibility_criteria');
        const previewDiv = document.getElementById('eligibility-preview');
        if (eligibilityField && previewDiv) {
            eligibilityField.addEventListener('input', function() {
                previewDiv.textContent = this.value || 'Preview: e.g., CGPA > 7.0 will check student CGPA.';
            });
        }

        // Password match checker for registration/confirm
        const password1 = document.getElementById('id_password1');
        const password2 = document.getElementById('id_password2');
        if (password1 && password2) {
            const updatePasswordFeedback = function() {
                const p1Val = password1.value;
                const p2Val = password2.value;
                if (p2Val.length > 0) {
                    if (p1Val === p2Val && p2Val.length >= 8) {
                        password2.classList.remove('is-invalid');
                        password2.classList.add('is-valid');
                        password2.setCustomValidity('');  // Clear validation message
                    } else {
                        password2.classList.add('is-invalid');
                        password2.classList.remove('is-valid');
                        if (p1Val !== p2Val) {
                            password2.setCustomValidity('Passwords do not match.');
                        } else if (p2Val.length < 8) {
                            password2.setCustomValidity('Password must be at least 8 characters.');
                        }
                    }
                } else {
                    password2.classList.remove('is-invalid', 'is-valid');
                    password2.setCustomValidity('');
                }
            };
            password1.addEventListener('input', updatePasswordFeedback);
            password2.addEventListener('input', updatePasswordFeedback);
        }

        // File upload preview for resume (profiles)
        const resumeInput = document.getElementById('id_resume_url');
        const resumePreview = document.getElementById('resume-preview');
        if (resumeInput && resumePreview) {
            resumeInput.addEventListener('change', function() {
                if (this.files[0]) {
                    const fileName = this.files[0].name;
                    resumePreview.textContent = `Selected: ${fileName}`;
                    if (!fileName.toLowerCase().endsWith('.pdf')) {
                        resumePreview.textContent += ' (Only PDF allowed - invalid file!)';
                        this.classList.add('is-invalid');
                        this.setCustomValidity('Please upload a PDF file only.');
                        alert('Only PDF files are allowed for resumes.');
                    } else {
                        this.classList.remove('is-invalid');
                        this.classList.add('is-valid');
                        this.setCustomValidity('');
                    }
                } else {
                    resumePreview.textContent = 'No file selected.';
                }
            });
        }

        // General form reset on error (optional: clears non-password fields if needed)
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('submit', function(e) {
                // If you want to clear on submit error (server-side), this is client-only
                if (this.querySelector('.is-invalid')) {
                    e.preventDefault();  // Prevent submit if client validation fails
                    alert('Please fix the errors before submitting.');
                }
            });
        });
    } catch (error) {
        console.error('Forms JS Error:', error);  // Graceful fallback
    }
});