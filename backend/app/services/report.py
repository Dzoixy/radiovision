def generate_medical_report(finding, confidence, side, vertical):

    if finding == "Pneumonia":
        return f"พบความผิดปกติบริเวณปอดด้าน{side} ส่วน{vertical} มีลักษณะเข้าได้กับ Pneumonia"

    elif finding == "Tuberculosis":
        return f"พบรอยโรคบริเวณปอดด้าน{side} ส่วน{vertical} มีลักษณะสงสัย Tuberculosis"

    elif finding == "COVID-19":
        return f"พบความผิดปกติลักษณะกระจายบริเวณปอดด้าน{side} ส่วน{vertical} เข้าได้กับ COVID-19 pneumonia"

    elif finding == "Mass":
        return f"พบลักษณะก้อนผิดปกติในปอดด้าน{side} ส่วน{vertical} สงสัย pulmonary mass"

    elif finding == "Atelectasis":
        return f"พบการแฟบของเนื้อปอดบริเวณด้าน{side} ส่วน{vertical} เข้าได้กับ atelectasis"

    else:
        return "ไม่พบความผิดปกติที่เด่นชัด"