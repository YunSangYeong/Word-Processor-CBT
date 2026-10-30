import { expect, test, type Page } from '@playwright/test';
async function openMenu(page: Page) {
  await page.getByRole('button',{name:'메뉴 열기',exact:true}).click();
  await expect(page.locator('.sidebar')).toHaveClass(/open/);
  await page.waitForTimeout(350);
}
async function touchSwipe(page: Page, down: boolean) {
  const session=await page.context().newCDPSession(page);
  const h=page.viewportSize()!.height;
  const start=down?h-70:90, end=down?90:h-70;
  await session.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:120,y:start}]});
  for(let i=1;i<=12;i++) {
    await session.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:120,y:start+(end-start)*i/12}]});
    await page.waitForTimeout(20);
  }
  await session.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});
  await session.detach();
  await page.waitForTimeout(200);
}
for(const size of [{width:390,height:480},{width:740,height:360},{width:390,height:480,large:true}]) {
  for(const input of ['wheel','touch'] as const) {
    test(`메뉴 실제 ${input} 아래·위·하단 도구·상단 선택 ${size.width}x${size.height}${size.large?' 글자확대':''}`,async({page,isMobile})=>{
      test.skip(!isMobile,'모바일 에뮬레이션 전용');
      await page.setViewportSize(size);await page.goto('');
      if(size.large) await page.addStyleTag({content:'.sidebar nav button,.sidebar .text-button {font-size:20px;line-height:1.7}.sidebar small,.sidebar p {font-size:16px;line-height:1.5}'});
      await openMenu(page);
      const sidebar=page.locator('.sidebar');
      expect(await sidebar.evaluate(el=>el.scrollHeight>el.clientHeight)).toBe(true);
      const backgroundY=await page.evaluate(()=>window.scrollY);
      await page.mouse.move(120,180);
      for(let i=0;i<5;i++) {
        if(input==='wheel') await page.mouse.wheel(0,400); else await touchSwipe(page,true);
      }
      await expect.poll(()=>sidebar.evaluate(el=>el.scrollTop)).toBeGreaterThan(0);
      await expect(page.getByRole('button',{name:'데이터 초기화',exact:true})).toBeInViewport();
      const download=page.waitForEvent('download');
      await page.getByRole('button',{name:'학습 기록 백업',exact:true}).click();
      expect((await download).suggestedFilename()).toBe('word-processor-study-backup.json');
      await page.getByRole('button',{name:'데이터 초기화',exact:true}).click();
      await expect(page.getByRole('dialog')).toBeVisible();
      await page.getByRole('button',{name:'돌아가기',exact:true}).click();
      await page.mouse.move(120,180);
      for(let i=0;i<6;i++) {
        if(input==='wheel') await page.mouse.wheel(0,-400); else await touchSwipe(page,false);
      }
      await expect.poll(()=>sidebar.evaluate(el=>el.scrollTop)).toBe(0);
      const dashboard=page.getByRole('navigation').getByRole('button',{name:'학습 대시보드',exact:true});
      await expect(dashboard).toBeInViewport();
      expect(await page.evaluate(()=>window.scrollY)).toBe(backgroundY);
      await page.screenshot({path:`test-results/menu-${input}-${size.width}-${size.height}${size.large?'-large':''}.png`});
      await dashboard.click();await expect(sidebar).not.toHaveClass(/open/);
      await expect(page.getByRole('heading',{name:'워드프로세서 필기 CBT',exact:true})).toBeVisible();
      expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
    });
  }
}
