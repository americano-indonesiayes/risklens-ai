from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from authentication.decorators import role_required
from .models import DocumentAnalysis
from .services import analyze_text, OpenAIAnalyzerError

@login_required(login_url='login')
@role_required("employee")
def show_document(request):
    latest_analysis = (
        DocumentAnalysis.objects.filter(user=request.user).order_by("-created_at").first()
    )

    if request.method == "POST":
        input_text = (request.POST.get("input_text") or "").strip()
        if not input_text:
            messages.error(request, "Input text tidak boleh kosong.")
        else:
            preview = input_text[:200]
            analysis = DocumentAnalysis.objects.create(
                user=request.user,
                input_text=input_text,
                input_preview=preview,
                status=DocumentAnalysis.Status.PENDING,
            )
            try:
                result = analyze_text(input_text)
                analysis.risk_level = result.get(
                    "risk_level", DocumentAnalysis.RiskLevel.SAFE
                )
                analysis.recommended_disclosure = result.get(
                    "recommended_disclosure",
                    DocumentAnalysis.Disclosure.INTERNAL_ONLY,
                )
                analysis.flag_reasons = result.get("flag_reasons", [])
                analysis.categories = result.get("categories", [])
                analysis.safe_version = result.get("safe_version", "")
                analysis.status = DocumentAnalysis.Status.COMPLETED
                analysis.save()
                latest_analysis = analysis
                messages.success(request, "Analisis berhasil dibuat.")
            except OpenAIAnalyzerError as exc:
                analysis.status = DocumentAnalysis.Status.FAILED
                analysis.save()
                messages.error(request, f"Gagal menganalisis teks: {exc}")

    context = {
        "latest_analysis": latest_analysis,
    }
    return render(request, "document.html", context)
