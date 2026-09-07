const { spawn } = require('child_process');

async function checkMobileScroll() {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new',
    '--remote-debugging-port=9666',
    '--disable-gpu',
    '--window-size=375,812'
  ]);

  await new Promise(r => setTimeout(r, 1500));

  try {
    const listRes = await fetch('http://127.0.0.1:9666/json');
    const tabs = await listRes.json();
    const pageTab = tabs.find(t => t.type === 'page');

    const ws = new WebSocket(pageTab.webSocketDebuggerUrl);
    await new Promise(r => ws.onopen = r);

    let id = 1;
    function send(method, params = {}) {
      return new Promise((resolve) => {
        const curId = id++;
        const handler = (event) => {
          const msg = JSON.parse(event.data);
          if (msg.id === curId) {
            ws.removeEventListener('message', handler);
            resolve(msg.result);
          }
        };
        ws.addEventListener('message', handler);
        ws.send(JSON.stringify({ id: curId, method, params }));
      });
    }

    await send('Emulation.setDeviceMetricsOverride', {
      width: 375,
      height: 812,
      deviceScaleFactor: 2,
      mobile: true
    });

    await send('Page.enable');
    await send('Page.navigate', { url: 'http://127.0.0.1:8080/' });

    await new Promise(r => setTimeout(r, 3000));

    // Scroll to the absolute bottom repeatedly
    await send('Runtime.evaluate', {
      expression: `(async () => {
        for (let i = 0; i < 10; i++) {
          window.scrollTo(0, document.documentElement.scrollHeight);
          await new Promise(r => setTimeout(r, 200));
        }
      })()`,
      awaitPromise: true
    });
    await new Promise(r => setTimeout(r, 1000));

    const evalRes = await send('Runtime.evaluate', {
      expression: `(() => {
        const footer = document.querySelector('.site-footer');
        const footerBottom = footer.getBoundingClientRect();
        const paymentMethods = document.querySelector('.payment-methods');
        const paymentRect = paymentMethods ? paymentMethods.getBoundingClientRect() : null;
        const copyEl = document.querySelector('.footer-bottom > div');
        const copyRect = copyEl ? copyEl.getBoundingClientRect() : null;
        const toolbar = document.querySelector('.mobile-toolbar');
        const toolbarRect = toolbar ? toolbar.getBoundingClientRect() : null;

        return {
          scrollY: window.scrollY,
          maxScrollY: document.documentElement.scrollHeight - window.innerHeight,
          viewportHeight: window.innerHeight,
          footerRect: {
            top: footerBottom.top,
            bottom: footerBottom.bottom,
            height: footerBottom.height
          },
          paymentRectBottom: paymentRect ? paymentRect.bottom : null,
          copyRectBottom: copyRect ? copyRect.bottom : null,
          toolbarRectTop: toolbarRect ? toolbarRect.top : null,
          // Distance from lowest content inside footer to bottom of viewport when fully scrolled
          blankSpaceUnderPaymentIcons: window.innerHeight - (paymentRect ? paymentRect.bottom : 0),
          blankSpaceUnderFooter: window.innerHeight - footerBottom.bottom
        };
      })()`,
      returnByValue: true
    });

    console.log('BOTTOM SCROLL DATA:', JSON.stringify(evalRes.result.value, null, 2));

    ws.close();
  } catch (e) {
    console.error(e);
  } finally {
    chrome.kill();
  }
}

checkMobileScroll();
