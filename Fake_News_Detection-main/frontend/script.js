// const newsText = document.getElementById("newsText");
// const characterCount = document.getElementById("characterCount");

// const analyzeBtn = document.getElementById("analyzeBtn");
// const buttonText = document.getElementById("buttonText");

// const resultCard = document.getElementById("resultCard");

// const prediction = document.getElementById("prediction");
// const confidenceValue =
//     document.getElementById("confidenceValue");

// const confidenceBar =
//     document.getElementById("confidenceBar");

// const resultMessage =
//     document.getElementById("resultMessage");

// const resultIcon =
//     document.getElementById("resultIcon");


// // Character counter

// newsText.addEventListener("input", () => {

//     const count = newsText.value.length;

//     characterCount.textContent =
//         `${count} characters`;

// });


// // Analyze button

// // analyzeBtn.addEventListener("click", async () => {

// //     const text = newsText.value.trim();

// //     if (!text) {

// //         alert("Please enter a news article or headline.");

// //         return;

// //     }


// //     // Loading state

// //     analyzeBtn.classList.add("loading");

// //     analyzeBtn.disabled = true;

// //     buttonText.textContent = "Analyzing...";


// //     /*
// //         TEMPORARY DEMO

// //         Later we will replace this section
// //         with a request to your Python backend.

// //         Example:

// //         const response = await fetch(
// //             "http://127.0.0.1:5000/predict",
// //             {
// //                 method: "POST",
// //                 headers: {
// //                     "Content-Type": "application/json"
// //                 },
// //                 body: JSON.stringify({
// //                     text: text
// //                 })
// //             }
// //         );

// //         const data = await response.json();
// //     */


// //     await new Promise(resolve =>
// //         setTimeout(resolve, 1500)
// //     );


// //     // Temporary prediction

// //     const isFake =
// //         Math.random() > 0.5;

// //     const confidence =
// //         Math.floor(
// //             Math.random() * 15 + 82
// //         );


// //     if (isFake) {

// //         prediction.textContent =
// //             "Likely Fake";

// //         resultIcon.textContent = "!";

// //         resultMessage.textContent =
// //             "The AI model detected linguistic patterns "
// //             + "that may be associated with misleading "
// //             + "or unreliable information.";

// //     } else {

// //         prediction.textContent =
// //             "Likely Real";

// //         resultIcon.textContent = "✓";

// //         resultMessage.textContent =
// //             "The AI model found patterns that are "
// //             + "more consistent with reliable news content.";

// //     }


// //     confidenceValue.textContent =
// //         `${confidence}%`;

// //     resultCard.classList.remove("hidden");


// //     setTimeout(() => {

// //         confidenceBar.style.width =
// //             `${confidence}%`;

// //     }, 100);


//     // Reset button

// //     analyzeBtn.classList.remove("loading");

// //     analyzeBtn.disabled = false;

// //     buttonText.textContent =
// //         "Analyze Again";

// // });
// analyzeBtn.addEventListener("click", async () => {

//     const text = newsText.value.trim();

//     if (!text) {

//         alert("Please enter a news article or headline.");

//         return;
//     }


//     // Loading state

//     analyzeBtn.classList.add("loading");

//     analyzeBtn.disabled = true;

//     buttonText.textContent = "Analyzing...";


//     try {

//         const response = await fetch(
//             "http://127.0.0.1:5000/predict",
//             {
//                 method: "POST",

//                 headers: {
//                     "Content-Type": "application/json"
//                 },

//                 body: JSON.stringify({
//                     text: text
//                 })
//             }
//         );


//         const data = await response.json();


//         if (!response.ok || !data.success) {

//             throw new Error(
//                 data.error ||
//                 "Prediction failed."
//             );

//         }


//         // Show result

//         resultCard.classList.remove("hidden");


//         const confidence =
//             data.confidence;


//         confidenceValue.textContent =
//             `${confidence}%`;


//         confidenceBar.style.width =
//             `${confidence}%`;


//         // REAL

//         if (data.prediction === "REAL") {

//             prediction.textContent =
//                 "Likely Real";

//             resultIcon.textContent =
//                 "✓";

//             resultMessage.textContent =
//                 "The AI model found patterns "
//                 + "that are more consistent with "
//                 + "reliable news content.";

//         }


//         // FAKE

//         else {

//             prediction.textContent =
//                 "Likely Fake";

//             resultIcon.textContent =
//                 "!";

//             resultMessage.textContent =
//                 "The AI model detected patterns "
//                 + "that may be associated with "
//                 + "misleading or unreliable information.";

//         }


//     } catch (error) {

//         console.error(error);

//         alert(
//             "Could not connect to the AI server.\n\n"
//             + "Make sure the Flask backend is running."
//         );

//     }


//     // Reset button

//     analyzeBtn.classList.remove(
//         "loading"
//     );

//     analyzeBtn.disabled = false;

//     buttonText.textContent =
//         "Analyze Again";

// });


const newsText = document.getElementById("newsText");
const characterCount = document.getElementById("characterCount");

const analyzeBtn = document.getElementById("analyzeBtn");
const buttonText = document.getElementById("buttonText");

const resultCard = document.getElementById("resultCard");

const prediction = document.getElementById("prediction");
const confidenceValue =
    document.getElementById("confidenceValue");

const confidenceBar =
    document.getElementById("confidenceBar");

const resultMessage =
    document.getElementById("resultMessage");

const resultIcon =
    document.getElementById("resultIcon");


// ==========================================
// CHARACTER COUNTER
// ==========================================

newsText.addEventListener("input", () => {

    const count = newsText.value.length;

    characterCount.textContent =
        `${count} characters`;

});


// ==========================================
// ANALYZE NEWS
// ==========================================

analyzeBtn.addEventListener("click", async () => {

    const text = newsText.value.trim();


    // Check empty input

    if (!text) {

        alert(
            "Please enter a news article or headline."
        );

        return;
    }


    // ======================================
    // LOADING STATE
    // ======================================

    analyzeBtn.classList.add(
        "loading"
    );

    analyzeBtn.disabled = true;

    buttonText.textContent =
        "Analyzing...";


    try {

        // ==================================
        // SEND REQUEST TO FLASK
        // ==================================

        const response = await fetch(
            "http://127.0.0.1:5000/predict",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    text: text
                })
            }
        );


        // Convert response to JSON

        const data =
            await response.json();


        // ==================================
        // CHECK SERVER RESPONSE
        // ==================================

        if (!response.ok ||
            !data.success) {

            throw new Error(
                data.error ||
                "Prediction failed."
            );

        }


        // ==================================
        // GET RESULT
        // ==================================

        const result =
            data.prediction;

        const confidence =
            data.confidence;


        // ==================================
        // SHOW RESULT CARD
        // ==================================

        resultCard.classList.remove(
            "hidden"
        );


        // ==================================
        // CONFIDENCE
        // ==================================

        confidenceValue.textContent =
            `${confidence}%`;


        confidenceBar.style.width =
            `${confidence}%`;


        // ==================================
        // REAL NEWS
        // ==================================

        if (result === "REAL") {

            prediction.textContent =
                "Likely Real";

            resultIcon.textContent =
                "✓";


            resultMessage.textContent =
                "The AI model found linguistic "
                + "patterns that are more consistent "
                + "with reliable news content.";

        }


        // ==================================
        // FAKE NEWS
        // ==================================

        else {

            prediction.textContent =
                "Likely Fake";

            resultIcon.textContent =
                "!";


            resultMessage.textContent =
                "The AI model detected linguistic "
                + "patterns that may be associated "
                + "with misleading or unreliable "
                + "information.";

        }


    }


    catch (error) {

        console.error(
            "Prediction error:",
            error
        );


        alert(
            "Unable to connect to the AI server.\n\n"
            + "Make sure Flask is running at "
            + "http://127.0.0.1:5000"
        );

    }


    finally {

        // ==================================
        // RESET BUTTON
        // ==================================

        analyzeBtn.classList.remove(
            "loading"
        );

        analyzeBtn.disabled = false;

        buttonText.textContent =
            "Analyze Again";

    }

});