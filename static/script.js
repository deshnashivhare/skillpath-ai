// Upload Resume (index.html)
async function uploadResume() {
  const input = document.getElementById("resume");

  input.click();

  input.onchange = async () => {
    const file = input.files[0];
    document.getElementById("fileName").innerText = file.name;

    // Fake response (for now)
    const data = {
      skills: ["Python", "Machine Learning", "SQL"],
      prediction: "80% chance in startups, 30% in MNCs"
    };

    localStorage.setItem("result", JSON.stringify(data));
    window.location.href = "dashboard.html";
  };
}


// Login Function (login.html)
function loginUser() {
  document.getElementById("errorMsg").classList.add("hidden");

  let email = document.getElementById("email").value.trim().toLowerCase();
  let password = document.getElementById("password").value;

  if (email === "admin" && password === "1234") {
    window.location.href = "dashboard.html";
  } else {
    document.getElementById("errorMsg").classList.remove("hidden");
  }
}

function showSignup() {
  const title = document.getElementById("formTitle");

  title.classList.remove("show");
  setTimeout(() => {
    title.innerText = "Welcome";
    title.classList.add("show");
  }, 150);

  document.getElementById("loginForm").classList.add("hidden");
  document.getElementById("signupForm").classList.remove("hidden");
}
