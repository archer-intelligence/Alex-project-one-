document.getElementById('generate-btn').addEventListener('click', async () => {
  const topic = document.getElementById('topic-input').value.trim();
  if (!topic) {
    alert('Please enter a topic');
    return;
  }
  document.getElementById('result').innerHTML = '<p>Generating…</p>';
  try {
    const response = await fetch('/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ topic })
    });
    if (!response.ok) {
      const err = await response.json();
      document.getElementById('result').innerHTML = `<p style="color:red;">Error: ${err.error}</p>`;
      return;
    }
    const data = await response.json();
    renderCurriculum(data.curriculum);
  } catch (e) {
    document.getElementById('result').innerHTML = `<p style="color:red;">Network error</p>`;
  }
});

function renderCurriculum(modules) {
  const container = document.getElementById('result');
  container.innerHTML = '';
  modules.forEach((mod) => {
    const modDiv = document.createElement('div');
    modDiv.innerHTML = `
      <h2>Module ${mod.module_number}: ${mod.title}</h2>
      <p>${mod.description}</p>
      <h3>Resources:</h3>
      <ul>
        ${mod.resources.map(r => `<li><a href="${r.url}" target="_blank">${r.description}</a></li>`).join('')}
      </ul>
      <p><strong>Exercise:</strong> ${mod.exercise}</p>
      <h3>Quiz:</h3>
      <ol>
        ${mod.quiz.map(q => `
          <li>
            <p><strong>Q:</strong> ${q.question}</p>
            <ul>
              ${q.answers.map((a, i) => `
                <li ${i === q.correct_answer_index ? 'style="font-weight:bold;"' : ''}>
                  ${a}
                </li>`).join('')}
            </ul>
          </li>`).join('')}
      </ol>
      <hr />
    `;
    container.appendChild(modDiv);
  });
}
