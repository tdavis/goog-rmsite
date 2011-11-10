#!/usr/bin/env python

import re
import argparse
import getpass
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


RE_HARD_DELETE = re.compile(r"JOT_purgeWebspace\('(.+?)'\)");


def extract_site_path_from_uri(domain, uri):
    """
    Return site path from a full URI.
    """
    i = uri.index(domain)
    fwd = len(domain)
    return uri[i+fwd:].strip('/')


def setup(domain):
    """
    Init driver; virtual display.
    """
    driver = webdriver.Firefox()
    driver.implicitly_wait(5)
    display = Display(visible=0, size=(1024, 768))
    display.start()
    return display, driver


def login(driver, user, passwd, count=0):
    """
    Login to Google; sometimes fails, so attempt up to 3 times.
    """
    driver.find_element_by_id("Email").clear()
    driver.find_element_by_id("Email").send_keys(user)
    driver.find_element_by_id("Passwd").clear()
    driver.find_element_by_id("Passwd").send_keys(passwd)
    driver.find_element_by_id("PersistentCookie").click()
    driver.find_element_by_id("signIn").click()

    if 'LoginAction' in driver.current_url and count < 3:
        return login(driver, user, passwd, count+1)
    elif count >= 3:
        return False
    return True


def soft_delete(driver, domain):
    """
    Initially delete a site; will show up in "deleted sites".
    """
    try:
        undeleted = driver.find_element_by_xpath("//*[@id='goog-ws-siteList']/div[2]/ul/li[1]/a")
    except NoSuchElementException:
        pass
    else:
        href = undeleted.get_attribute("href")
        driver.get(href)
        driver.find_element_by_id("more-actions-btn-label").click()
        driver.find_element_by_css_selector("#openManageSite > div.goog-menuitem-content").click()
        #driver.find_element_by_link_text("General").click()
        driver.find_element_by_id("sites-deleteLink").click()
        driver.find_element_by_xpath("//a[@id=':4.okBtn']/div/div/div/div/div[2]").click()

        return extract_site_path_from_uri(domain, href)


def hard_delete(driver, domain):
    """
    Final deletion; remove site entirely.
    """
    try:
        div = driver.find_element_by_xpath("//div[@onclick[substring(.,1,18)='JOT_purgeWebspace(']]")
        div.click()
        driver.find_element_by_xpath("//a[@id[substring(.,string-length()-4)='okBtn']]/div/div/div/div/div[2]").click()
        return RE_HARD_DELETE.search(div.get_attribute("onclick")).groups()[0]
    except NoSuchElementException:
        return False


def options():
    """
    Parse CLI arguments.
    """
    parser = argparse.ArgumentParser(description='Delete some Google Sites')
    parser.add_argument('domain', metavar='DOMAIN', type=str,
                       help='Domain to delete from')
    parser.add_argument('--username', '-u', dest='user', action='store',
                       type=str, help='Username of person to login as')
    parser.add_argument('--password', '-w', dest='password', action='store',
                       type=str, help='Password of person to login as; leave '
                        'out for prompt')
    parser.add_argument('-c', '--count', dest='count',
                        type=int, default=1,
                        help='Max number of sites to delete (default: 1)')
    args = parser.parse_args()
    return args


def main():
    count = 0
    opts = options()

    if not opts.password:
        opts.password = getpass.getpass()

    display, driver = setup(opts.domain)
    base_url = "https://sites.google.com/a/%s" % opts.domain

    print 'Deleting up to %d site(s) on %s as %s.' % (opts.count, opts.domain,
                                                      opts.user)

    try:
        driver.get(base_url)
        success = login(driver, opts.user, opts.password)
        if success:
            print 'Login successful.'
            while True:
                driver.get(base_url)
                soft_result = soft_delete(driver, opts.domain)
                if soft_result:
                    print 'Site "%s" soft-deleted.' % soft_result
                else:
                    print 'No site to soft delete!'

                driver.get(base_url)
                hard_result = hard_delete(driver, opts.domain)
                if hard_result:
                    print 'Site "%s" hard-deleted.' % hard_result
                else:
                    print 'No site to hard delete!'

                count += 1
                if (not soft_result and not hard_result) or count >= opts.count:
                    break
        else:
            print 'Login failed!'
    finally:
        driver.quit()
        display.stop()

if __name__ == "__main__":
    main()
    print 'done'	
