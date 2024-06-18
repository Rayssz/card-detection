$(document).ready(function () {
    const video = document.getElementById('video');
    const predictionResult = document.getElementById('predictionResult');

    // Check if the browser supports accessing the camera
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        // Access the camera
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function (stream) {
                // If access is granted, set the video source to the stream
                video.srcObject = stream;
            })
            .catch(function (error) {
                // If there's an error accessing the camera, log it to the console
                console.log("Something went wrong with accessing the camera!", error);
            });
    } else {
        // If the browser doesn't support accessing the camera, log it to the console
        console.log("getUserMedia is not supported by this browser");
    }

    // Function to take a snapshot from the video stream
    $('#snap').click(function () {
        const canvas = document.getElementById('canvas');
        const context = canvas.getContext('2d');

        // Set the canvas size to match the video frame size
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        // Draw the current frame from the video onto the canvas
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        // Convert the canvas content to a data URL representing a PNG image
        const dataUrl = canvas.toDataURL('image/png');

        // Send the captured image data to the server for prediction
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: JSON.stringify({ image: dataUrl.split(',')[1] }),
            contentType: 'application/json',
            success: function (response) {
                // Display the prediction result on the page
                predictionResult.innerHTML = 'Prediction: <span class="' + response.prediction + '">' + response.prediction + '</span>';
            },
            error: function (xhr, status, error) {
                // Log any errors that occur during the AJAX request
                console.log("Error sending image data for prediction:", error);
            }
        });
    });
});
