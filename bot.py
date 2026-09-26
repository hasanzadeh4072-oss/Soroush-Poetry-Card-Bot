def send_card_report(
    user_id,
    username,
    full_name,
    poem,
    design,
    color
):

    """
    ارسال مستقل گزارش کارت.

    این بخش جدا از روند ساخت کارت اجرا می‌شود.
    اگر بات ناشناس خواب باشد، تلاش مجدد انجام می‌شود.
    """

    payload = {
        "user_id": user_id,
        "username": username,
        "full_name": full_name,
        "poem": poem,
        "design": design,
        "color": color
    }

    headers = {
        "X-Card-Report-Secret": CARD_REPORT_SECRET
    }

    for attempt in range(1, 4):

        try:

            print(
                f"CARD REPORT ATTEMPT {attempt}",
                flush=True
            )

            response = session().post(
                ANONYMOUS_REPORT_URL,
                json=payload,
                headers=headers,
                timeout=30
            )

            print(
                f"CARD REPORT STATUS {attempt}: "
                f"{response.status_code}",
                flush=True
            )

            print(
                f"CARD REPORT RESPONSE {attempt}: "
                f"{response.text}",
                flush=True
            )

            if response.ok:

                print(
                    "CARD REPORT DELIVERED",
                    flush=True
                )

                return

        except Exception as error:

            print(
                f"CARD REPORT ERROR {attempt}: "
                f"{repr(error)}",
                flush=True
            )

        # فرصت برای بیدار شدن Render
        if attempt == 1:

            print(
                "CARD REPORT WAITING 70s FOR RENDER",
                flush=True
            )

            time.sleep(70)

        elif attempt == 2:

            time.sleep(10)

    print(
        "CARD REPORT FAILED AFTER 3 ATTEMPTS",
        flush=True
    )
