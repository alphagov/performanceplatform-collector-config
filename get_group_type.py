#!/usr/bin/env python
# encoding: utf-8
import json

files = [
    "queries/accelerated-possession-eviction/journey-completions.json",
    "queries/accelerated-possession-eviction/journey-starts.json",
    "queries/blood-donor-appointments/browser-usage.json",
    "queries/blood-donor-appointments/completion-by-goal.json",
    "queries/blood-donor-appointments/conversions-by-keyword.json",
    "queries/blood-donor-appointments/conversions-by-landing-page.json",
    "queries/blood-donor-appointments/conversions-by-medium.json",
    "queries/blood-donor-appointments/conversions-by-social-network.json",
    "queries/blood-donor-appointments/conversions-by-source.json",
    "queries/blood-donor-appointments/device-usage.json",
    "queries/blood-donor-appointments/journey-by-goal-booking-completion.json",
    "queries/blood-donor-appointments/journey-by-goal-booking-start.json",
    "queries/blood-donor-appointments/journey-by-goal-registration-completion.json",
    "queries/blood-donor-appointments/journey-by-goal-registration-start.json",
    "queries/blood-donor-appointments/journey-by-goal-session-finder.json",
    "queries/blood-donor-appointments/journey-by-goal-site-starts.json",
    "queries/blood-donor-appointments/new-returning-count.json",
    "queries/carers-allowance/journey.json",
    "queries/carers-allowance/organic-rate.json",
    "queries/carers-allowance/referrers-rate.json",
    "queries/carers-allowance/social-rate.json",
    "queries/carers-allowance/time-taken-to-complete.json",
    "queries/digital-marketplace/browsers.json",
    "queries/digital-marketplace/devices.json",
    "queries/digital-marketplace/traffic-count.json",
    "queries/driving-test-practical-public/device-usage.json",
    "queries/driving-test-practical-public/journey-help.json",
    "queries/driving-test-practical-public/journey.json",
    "queries/employment-tribunal-applications/browser-usage.json",
    "queries/employment-tribunal-applications/device-usage.json",
    "queries/employment-tribunal-applications/journey-by-page-complete.json",
    "queries/employment-tribunal-applications/journey-by-page-eligibility.json",
    "queries/employment-tribunal-applications/journey-by-page-start.json",
    "queries/employment-tribunal-applications/new-returning-count.json",
    "queries/govuk/browsers.json",
    "queries/govuk/devices.json",
    "queries/govuk/most_viewed.json",
    "queries/govuk/most_viewed_news.json",
    "queries/govuk/most_viewed_policies.json",
    "queries/govuk/visitors.json",
    "queries/govuk-info/page-statistics.json",
    "queries/govuk-info/search-terms.json",
    "queries/insidegov/visitors.json",
    "queries/lasting-power-of-attorney/journey.json",
    "queries/legal-aid-civil-claims/browser-usage.json",
    "queries/legal-aid-civil-claims/device-usage.json",
    "queries/licensing/browsers.json",
    "queries/licensing/devices.json",
    "queries/licensing/journey.json",
    "queries/pay-foreign-marriage-certificates/journey.json",
    "queries/pay-legalisation-drop-off/journey.json",
    "queries/pay-legalisation-post/journey.json",
    "queries/pay-register-birth-abroad/journey.json",
    "queries/pay-register-death-abroad/journey.json",
    "queries/paye-employee-company-car/browser-usage.json",
    "queries/paye-employee-company-car/device-usage.json",
    "queries/paye-employee-company-car/new-returning-count.json",
    "queries/performance-platform/browsers.json",
    "queries/performance-platform/devices.json",
    "queries/performance-platform/traffic-count.json",
    "queries/police-uk-postcode-search/browser-usage.json",
    "queries/police-uk-postcode-search/device-usage.json",
    "queries/police-uk-postcode-search/new-returning-count.json",
    "queries/prison-visits/device-usage.json",
    "queries/prison-visits/journey.json",
    "queries/renewtaxcredits/device-usage.json",
    "queries/renewtaxcredits/journey.json",
    "queries/service-submission-portal/browsers.json",
    "queries/service-submission-portal/devices.json",
    "queries/service-submission-portal/traffic-count.json",
    "queries/student-finance/browser-usage.json",
    "queries/student-finance/device-usage.json",
    "queries/student-finance/journey.json",
    "queries/student-finance/new-returning-users.json",
    "queries/student-finance/site-traffic.json",
    "queries/tax-vat-content/devices-count.json",
    "queries/tax-vat-content/new-returning-count.json",
    "queries/tax-vat-content/organic-rate.json",
    "queries/tax-vat-content/pageviews-count.json",
    "queries/tax-vat-content/referrers-rate.json",
    "queries/tax-vat-content/social-rate.json",
    "queries/tax-vat-content/top-count.json",
    "queries/tax-vat-content/traffic-count.json",
    "queries/tier-2-visit-visa/devices.json",
    "queries/tier-2-visit-visa/journey.json",
    "queries/tier-2-visit-visa/volumetrics.json",
    "queries/view-driving-record/devices.json",
    "queries/view-driving-record/digital-transactions.json"
]

if __name__ == '__main__':
    for file_name in files:
        with open(file_name, "r") as f:
            the_dict = json.loads(f.read())
            if 'options' in the_dict:
                if 'idMapping' in the_dict['options']:
                    print 'skipping {}'.format(file_name)
                elif 'plugins' in the_dict['options']:
                    id_specified = False
                    for plugin in the_dict['options']['plugins']:
                        if 'ComputeIdFrom' in plugin:
                            id_specified = True
                    if id_specified:
                        print 'skipping {}'.format(file_name)
                    else:
                        print the_dict['data-set']
                else:
                    print the_dict['data-set']
            else:
                print the_dict['data-set']
