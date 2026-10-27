/**
 * Finery Room — Luxury Beauty Experience
 * Frontend Interactions & Navigation Logic
 * Tati Siding, Botswana
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Elements
  const header = document.getElementById('siteHeader');
  const mobileToggle = document.getElementById('mobileToggle');
  const mobileDrawer = document.getElementById('mobileDrawer');
  const mobileNavLinks = document.querySelectorAll('.mobile-nav-link');
  const vipForm = document.getElementById('vipForm');
  const vipInput = document.getElementById('vipName');
  const vipNotice = document.getElementById('vipNotice');
  const faqAssistantForm = document.getElementById('faqAssistantForm');
  const faqQuestion = document.getElementById('faqAssistantQuestion');
  const faqHoneypot = document.getElementById('faqAssistantWebsite');
  const faqStatus = document.getElementById('faqAssistantStatus');
  const faqReply = document.getElementById('faqAssistantReply');
  const faqAnswer = document.getElementById('faqAssistantAnswer');
  const faqWhatsApp = document.getElementById('faqAssistantWhatsApp');
  const faqSubmit = faqAssistantForm?.querySelector('button[type="submit"]');

  // 2. Header Scroll Effect
  let lastScrollY = window.scrollY;
  const updateHeaderScroll = () => {
    if (window.scrollY > 40) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  };

  window.addEventListener('scroll', updateHeaderScroll, { passive: true });
  updateHeaderScroll();

  // 3. Mobile Drawer Toggle
  if (mobileToggle && mobileDrawer) {
    const toggleDrawer = () => {
      const isOpen = mobileDrawer.classList.contains('open');
      if (isOpen) {
        mobileDrawer.classList.remove('open');
        mobileToggle.setAttribute('aria-expanded', 'false');
        mobileDrawer.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
      } else {
        mobileDrawer.classList.add('open');
        mobileToggle.setAttribute('aria-expanded', 'true');
        mobileDrawer.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
      }
    };

    mobileToggle.addEventListener('click', toggleDrawer);

    // Close drawer when any mobile nav link is clicked
    mobileNavLinks.forEach(link => {
      link.addEventListener('click', () => {
        if (mobileDrawer.classList.contains('open')) {
          toggleDrawer();
        }
      });
    });
  }

  // 4. VIP Form Re-marketing Submission
  if (vipForm && vipInput) {
    vipForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const val = vipInput.value.trim();
      if (!val) return;

      if (vipNotice) {
        vipNotice.style.display = 'block';
        vipNotice.textContent = 'Redirecting to WhatsApp to confirm your VIP list spot...';
      }

      const encodedMsg = encodeURIComponent(
        `Hi Finery Room, please add me to your VIP WhatsApp list for first-look promos and specials! (Name/Contact: ${val})`
      );
      const whatsappUrl = `https://wa.me/26776584100?text=${encodedMsg}`;

      setTimeout(() => {
        window.open(whatsappUrl, '_blank', 'noopener,noreferrer');
        vipInput.value = '';
        if (vipNotice) {
          vipNotice.textContent = 'Thank you! Your WhatsApp message has been prepared.';
        }
      }, 600);
    });
  }

  // 5. Website FAQ assistant. The form sends only a short question to n8n.
  if (faqAssistantForm && faqQuestion && faqStatus && faqReply && faqAnswer && faqWhatsApp && faqSubmit) {
    const webhookUrl = String(window.FineryRoomFaqConfig?.webhookUrl || '').trim();
    let lastQuestionAt = 0;

    faqAssistantForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const question = faqQuestion.value.trim();

      if (faqHoneypot?.value.trim()) return;
      if (!question || question.length > 500) {
        faqStatus.textContent = 'Please enter a question under 500 characters.';
        return;
      }
      if (/[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}/.test(question) || /\+?\d[\d\s().-]{6,}\d/.test(question)) {
        faqStatus.textContent = 'Please remove email addresses or phone numbers from your question.';
        return;
      }
      if (Date.now() - lastQuestionAt < 8000) {
        faqStatus.textContent = 'Please wait a few seconds before asking another question.';
        return;
      }
      lastQuestionAt = Date.now();
      faqStatus.textContent = '';
      faqReply.hidden = true;
      faqWhatsApp.hidden = true;
      faqSubmit.disabled = true;
      faqSubmit.setAttribute('aria-busy', 'true');
      faqSubmit.textContent = 'Finding an answer…';

      try {
        if (!webhookUrl) throw new Error('Assistant endpoint is not configured.');
        const endpoint = new URL(webhookUrl);
        const localPreview = ['localhost', '127.0.0.1'].includes(window.location.hostname);
        if (endpoint.protocol !== 'https:' && !localPreview) throw new Error('Secure endpoint required.');

        const response = await fetch(endpoint.href, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ question, website: faqHoneypot?.value || '' }),
          credentials: 'omit',
          cache: 'no-store',
          mode: 'cors'
        });
        if (!response.ok) throw new Error('FAQ service returned an error.');
        const data = await response.json();
        if (typeof data.answer !== 'string' || !data.answer.trim()) throw new Error('FAQ service did not return an answer.');

        faqAnswer.textContent = data.answer.trim();
        faqReply.hidden = false;
        faqWhatsApp.hidden = false;
        faqStatus.textContent = data.needsHuman
          ? 'For booking or a personal enquiry, our team can help on WhatsApp.'
          : 'If you need anything else, message our team on WhatsApp.';
      } catch {
        faqStatus.textContent = 'The quick answer service is unavailable just now. You can send your question to our team on WhatsApp.';
        faqWhatsApp.href = `https://wa.me/26776584100?text=${encodeURIComponent(`Hi Finery Room, I have a question: ${question}`)}`;
        faqWhatsApp.hidden = false;
        faqReply.hidden = false;
        faqAnswer.textContent = 'Our team will be happy to help you directly.';
      } finally {
        faqSubmit.disabled = false;
        faqSubmit.removeAttribute('aria-busy');
        faqSubmit.textContent = 'Get an answer';
      }
    });
  }

  // 6. Enhance Accordion Accessibility (FAQ)
  const faqItems = document.querySelectorAll('.faq-item');
  faqItems.forEach(item => {
    item.addEventListener('toggle', () => {
      if (item.open) {
        // Optional: close other open items for a cleaner accordion feel
        faqItems.forEach(otherItem => {
          if (otherItem !== item && otherItem.open) {
            otherItem.open = false;
          }
        });
      }
    });
  });

  // 7. Log confirmation for studio support
  console.log('Finery Room website initialized. Booking line: +267 765 841 00 (Tati Siding, Botswana)');
});
