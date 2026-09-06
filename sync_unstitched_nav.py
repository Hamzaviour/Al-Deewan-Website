import glob, re

files = glob.glob('*.html')
unstitched_block = """          <div class="nav-item-dropdown" id="nav-dropdown-unstitched">
            <a href="collections.html?category=Unstitched" class="header-nav__link">
              UNSTITCHED
              <svg class="nav-arrow-down" width="10" height="6" viewBox="0 0 10 6" fill="currentColor"><path d="M0 0.5L5 5.5L10 0.5H0Z"/></svg>
            </a>
            <ul class="nav-dropdown-menu">
              <li class="nav-dropdown-item has-submenu">
                <a href="collections.html?category=Unstitched&type=1PC" class="nav-dropdown-link">
                  <span>1PC</span>
                  <svg class="nav-arrow-right" width="6" height="10" viewBox="0 0 6 10" fill="currentColor"><path d="M0.5 0L5.5 5L0.5 10V0Z"/></svg>
                </a>
                <ul class="nav-submenu">
                  <li><a href="collections.html?category=Unstitched&type=1PC&season=Winter" class="nav-dropdown-link">Winter</a></li>
                  <li><a href="collections.html?category=Unstitched&type=1PC&season=Summer" class="nav-dropdown-link">Summer</a></li>
                  <li><a href="collections.html?type=Bedsheet" class="nav-dropdown-link">Bedsheets</a></li>
                </ul>
              </li>
              <li class="nav-dropdown-item has-submenu">
                <a href="collections.html?category=Unstitched&type=2PC" class="nav-dropdown-link">
                  <span>2PC</span>
                  <svg class="nav-arrow-right" width="6" height="10" viewBox="0 0 6 10" fill="currentColor"><path d="M0.5 0L5.5 5L0.5 10V0Z"/></svg>
                </a>
                <ul class="nav-submenu">
                  <li><a href="collections.html?category=Unstitched&type=2PC&season=Winter" class="nav-dropdown-link">Winter</a></li>
                  <li><a href="collections.html?category=Unstitched&type=2PC&season=Summer" class="nav-dropdown-link">Summer</a></li>
                </ul>
              </li>
              <li class="nav-dropdown-item has-submenu">
                <a href="collections.html?category=Unstitched&type=3PC" class="nav-dropdown-link">
                  <span>3PC</span>
                  <svg class="nav-arrow-right" width="6" height="10" viewBox="0 0 6 10" fill="currentColor"><path d="M0.5 0L5.5 5L0.5 10V0Z"/></svg>
                </a>
                <ul class="nav-submenu">
                  <li><a href="collections.html?category=Unstitched&type=3PC&season=Winter" class="nav-dropdown-link">Winter</a></li>
                  <li><a href="collections.html?category=Unstitched&type=3PC&season=Summer" class="nav-dropdown-link">Summer</a></li>
                </ul>
              </li>
            </ul>
          </div>"""

for f in files:
    if f in ['admin.html', 'firecrawl_homepage.html', 'homepage.html']:
        continue
    with open(f, 'r', encoding='utf-8') as fp:
        c = fp.read()
    if 'id="nav-dropdown-unstitched"' in c:
        # replace the entire div with id="nav-dropdown-unstitched"
        c_new = re.sub(r'<div class="nav-item-dropdown" id="nav-dropdown-unstitched">[\s\S]*?</ul>\s*</div>', unstitched_block, c, count=1)
        if c_new != c:
            with open(f, 'w', encoding='utf-8') as fp:
                fp.write(c_new)
            print('Updated:', f)
        else:
            print('Already up-to-date:', f)
