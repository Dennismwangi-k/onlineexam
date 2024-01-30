document.addEventListener('DOMContentLoaded', function() {
    // Get the current year
    var currentYear = new Date().getFullYear();

    // Set the current year to the element with id 'currentYear'
    document.getElementById('currentYear').textContent = currentYear;
});