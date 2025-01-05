document.addEventListener('DOMContentLoaded', function() {
    const translateBtn = document.getElementById('translateBtn');
    const sourceText = document.getElementById('sourceText');
    const targetText = document.getElementById('targetText');
    const sourceLang = document.getElementById('sourceLang');
    const targetLang = document.getElementById('targetLang');
    const translationStyle = document.getElementById('translationStyle');

    translateBtn.addEventListener('click', async function() {
        if (!sourceText.value.trim()) {
            alert('Пожалуйста, введите текст для перевода');
            return;
        }

        translateBtn.disabled = true;
        translateBtn.textContent = 'Переводим...';

        try {
            const response = await fetch('/translate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: sourceText.value,
                    source_lang: sourceLang.value,
                    target_lang: targetLang.value,
                    style: translationStyle.value
                })
            });

            const data = await response.json();

            if (data.error) {
                throw new Error(data.error);
            }

            targetText.value = data.translation;

        } catch (error) {
            alert('Ошибка при переводе: ' + error.message);
        } finally {
            translateBtn.disabled = false;
            translateBtn.textContent = 'Перевести';
        }
    });

    // Автоматическое переключение языков
    sourceLang.addEventListener('change', function() {
        targetLang.value = sourceLang.value === 'русский' ? 'английский' : 'русский';
    });

    targetLang.addEventListener('change', function() {
        sourceLang.value = targetLang.value === 'русский' ? 'английский' : 'русский';
    });
});