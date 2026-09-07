const { spawn } = require('child_process');

async function testMobile() {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new',
    '--remote-debugging-port=9444',
    '--disable-gpu',
    '--window-size=375,812'
  ]);

  await new Promise(r => setTimeout(r, 1500));

  try {
    const listRes = await fetch('http://127.0.0.1:9444/json');
    const tabs = await listRes.json();
    const pageTab = tabs.find(t => t.type === 'page');
    if (!pageTab) {
      console.log('No page tab');
      chrome.kill();
      return;
    }

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

    // Wait for page to fully load
    await new Promise(r => setTimeout(r, 3000));

    const evalRes = await send('Runtime.evaluate', {
      expression: `(() => {
        const scrollW = document.documentElement.scrollWidth;
        const innerW = window.innerWidth;
        const bodyScrollW = document.body.scrollWidth;

        const overflowingRight = [];
        document.querySelectorAll('*').forEach(el => {
          const rect = el.getBoundingClientRect();
          if (rect.right > innerW + 1) {
            const cs = window.getComputedStyle(el);
            if (cs.position !== 'fixed') {
              overflowingRight.push({
                tag: el.tagName,
                id: el.id,
                className: el.className,
                right: rect.right,
                width: rect.width
              });
            }
          }
        });

        return {
          innerW,
          scrollW,
          bodyScrollW,
          hasHorizontalOverflow: scrollW > innerW,
          overflowingCount: overflowingRight.length,
          overflowingSample: overflowingRight.slice(0, 10)
        };
      })()`,
      returnByValue: true
    });

    console.log('RESULT:', JSON.stringify(evalRes.result.value, null, 2));

    ws.close();
  } catch (e) {
    console.error(e);
  } finally {
    chrome.kill();
  }
}

testMobile();
