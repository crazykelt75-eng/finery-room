# Finery Room FAQ assistant integration

This local site patch adds an optional “Ask Finery Room” form below the existing FAQ. It sends one short question to an n8n HTTPS webhook and displays a returned answer. The form does not request a name or phone number. It blocks obvious email addresses and phone numbers, limits questions to 500 characters, includes a hidden honeypot, and throttles repeat submissions in the current page session.

## Webhook contract

Request:

```json
{
  "question": "How much is a two-week lash refill?",
  "website": ""
}
```

Response:

```json
{
  "answer": "A two-week lash refill is P40.",
  "needsHuman": false
}
```

`needsHuman` is set for booking-type questions in the current draft. The interface always offers WhatsApp as a human follow-up. The workflow must never promise appointment availability or invent opening hours.

## Endpoint and rollout

The production URL is staged in `faq-assistant-config.js` as `https://neosale.app.n8n.cloud/webhook/finery-room-faq`. The copied “Finery Room Website FAQ” workflow returned valid JSON in two successful end-to-end synthetic tests: a two-week lash refill returned P40 with `needsHuman: false`, and a booking question returned `needsHuman: true` with a WhatsApp handoff. The workflow is still a draft and inactive, so this production URL is not ready for public traffic.

Before launch, verify the actual production website HTTPS origin and DNS. The configured `https://fineryroom.bw/` address did not resolve when checked during setup. Set the webhook's CORS allow-list to the confirmed production origin; do not use `*` for the public endpoint. Publish/activate the workflow and deploy this patch only after the user confirms those public-facing actions. After deployment, test the public form with synthetic questions.

## Privacy and handoff

The front end transmits only the question and the honeypot field. The browser rejects obvious email addresses and phone numbers, but these checks can be bypassed by a direct caller; they are not server-side abuse protection. n8n execution logs and the connected language model may process submitted text, so the public form tells visitors not to include private details. WhatsApp links open a prefilled draft that the visitor can review before sending; the form does not send a WhatsApp message automatically. No public website deployment or live customer request has been tested.
