// Keep links to sections of the former single page working.
const legacyPages = {
  '#research': 'research.html',
  '#publications': 'publications.html',
  '#cv': 'cv.html',
  '#art': 'art.html',
  '#contact': 'contact.html'
};
function followLegacyLink() {
  const destination = legacyPages[window.location.hash];
  if (destination) window.location.replace(destination);
}
followLegacyLink();
window.addEventListener('hashchange', followLegacyLink);
