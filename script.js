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

  // 5. Enhance Accordion Accessibility (FAQ)
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

  // 6. Log confirmation for studio support
  console.log('Finery Room website initialized. Booking line: +267 765 841 00 (Tati Siding, Botswana)');
});
