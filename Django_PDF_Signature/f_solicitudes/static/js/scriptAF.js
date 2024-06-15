	
		// IMPORTANTE: PARA PRUEBAS, USAR SIEMPRE UNA IP O NOMBRE DE DOMINIO, NUNCA 'LOCALHOST' O '127.0.0.1'
		// SI NO SE HACE ASI, AUTOFIRMA BLOQUEARA LA FIRMA POR SEGURIDAD
		function saveSignature() {
			AutoScript.saveDataToFile(
					document.getElementById('result').value,
					"Guardar firma electr\u00F3nica",
					"prueba.csig",
					null,
					null,
					showSaveOkCallback,
					showErrorCallback);
		}
	
		function showSaveOkCallback() {
			showLog("Guardado OK");
		}
		
		function showSignResultCallback(signatureB64, certificateB64, extraData) {
			showLog("Firma OK");
			if (extraData) {
				var extras = JSON.parse(extraData);
				showLog("Fichero cargado: " + extras.filename);
			}

			// Mostramos el certificado Base 64
			//showLog("Certificado:\n" + certificateB64);

			// A modo ilustrativo, mostramos la firma Base 64 en el formulario
			document.getElementById('result').value = signatureB64;
			
			// Agregamos la firma a un campo oculto para enviarla junto al formulario
			document.getElementById('resultField').value = signatureB64;
		}
		
		function showCertCallback(certificateB64) {
			showLog("Certificado seleccionado");
			document.getElementById('result').value = certificateB64;
		}
		
		function showErrorCallback(errorType, errorMessage) {
			showLog("Type: " + errorType + "\nMessage: " + errorMessage);
		}

		function doSign() {			
			try {
				var data = document.getElementById("data").value;
				AutoScript.sign(
					(data != undefined && data != null && data != "") ? data : null,
					document.getElementById("algorithm").value,
					document.getElementById("format").value,
					document.getElementById("params").value,
					showSignResultCallback,
					showErrorCallback);
				
			} catch(e) {
				try {
					showLog("Type: " + AutoScript.getErrorType() + "\nMessage: " + AutoScript.getErrorMessage());
				} catch(ex) {
					showLog("Error: " + e);
				}
			}
		}
		
		function downloadAndSign() {
			try {

				AutoScript.downloadRemoteData(
						document.location,
						downloadedSuccessCallback,
						downloadedErrorCallback);
			} catch(e) {
				showLog("Error en la descarga de los datos: " + e);
			}
		}
		
		function downloadedSuccessCallback(data) {
			try {
				AutoScript.sign(
					(data != undefined && data != null && data != "") ? data : null,
					document.getElementById("algorithm").value,
					document.getElementById("format").value,
					document.getElementById("params").value,
					showSignResultCallback,
					showErrorCallback);
			} catch(e) {
				try {
					showLog("Type: " + AutoScript.getErrorType() + "\nMessage: " + AutoScript.getErrorMessage());
				} catch(ex) {
					showLog("Error: " + e);
				}
			}
		}
		
		function downloadedErrorCallback(e) {
			showLog("Error en la descarga de los datos: " + e);
		}
		
		function doCoSign() {
			try {
				var signature = document.getElementById("signature").value;
				var data = document.getElementById("data").value;

				AutoScript.coSign(
					(signature != undefined && signature != null && signature != "") ? signature : null,
					(data != undefined && data != null && data != "") ? data : null,
					document.getElementById("algorithm").value,
					document.getElementById("format").value,
					document.getElementById("params").value,
					showSignResultCallback,
					showErrorCallback);

			} catch(e) {
				showLog("Type: " + AutoScript.getErrorType() + "\nMessage: " + AutoScript.getErrorMessage());
			}
		}

		function doCounterSign() {
			try {
				var signature = document.getElementById("signature").value;

				AutoScript.counterSign(
					(signature != undefined && signature != null && signature != "") ? signature : null,
					document.getElementById("algorithm").value,
					document.getElementById("format").value,
					document.getElementById("params").value,
					showSignResultCallback,
					showErrorCallback);
			} catch(e) {
				showLog("Type: " + AutoScript.getErrorType() + "\nMessage: " + AutoScript.getErrorMessage());
			}
		}

		function doSelectCert() {
			try {
				AutoScript.selectCertificate(
					document.getElementById("params").value,
					showCertCallback,
					showErrorCallback);
			} catch(e) {
				showLog("Type: " + AutoScript.getErrorType() + "\nMessage: " + AutoScript.getErrorMessage());
			}
		}

		function doSignAndSave(cryptoOp) {
			
			try {				
				var data;
				if (cryptoOp == 'sign') {
					data = document.getElementById("data").value;
				}
				else {
					data = document.getElementById("signature").value;
				}

				AutoScript.signAndSaveToFile(
					cryptoOp,
					(data != undefined && data != null && data != "") ? data : null,
					document.getElementById("algorithm").value,
					document.getElementById("format").value,
					document.getElementById("params").value,
					null,
					showSignResultCallback,
					showErrorCallback);

			} catch(e) {
				try {
					showLog("Type: " + AutoScript.getErrorType() + "\nMessage: " + AutoScript.getErrorMessage());
				} catch(ex) {
					showLog("Error: " + e);
				}
			}
		}
		
		
		function showAppletLog() {
			try {
				AutoScript.getCurrentLog(showGetCurrentLogResultCallback,
						showErrorCallback);
			} catch (e) {
				showLog("Type: " + AutoScript.getErrorType() + "\nMessage: "
						+ AutoScript.getErrorMessage());
			}
		}

		function showGetCurrentLogResultCallback(log) {
			showLog(log)
		}

		
		/**
		 * Funcion para la carga de un fichero. Almacena el contenido del fichero en un campo oculto y muestra su nombre.
		 * LA CARGA INDEPENDIENTE DE FICHEROS DEBE EVITARSE EN LA MEDIDA DE LO POSIBLE, DADO QUE NO ES COMPATIBLE CON EL
		 * CLIENTE MOVIL NI CON AUTOFIRMA EN EDGE NI INTERNET EXPLORER 10 O ANTERIORES. Si deseas firmar, cofirmar o
		 * contrafirmar un fichero, llama al metodo correspondiente (sign(), coSign() o counterSign()) sin indicar los datos.
		 */
		function browseDatos(title) {
			try {
				AutoScript.getFileNameContentBase64(
						title,
						null,
						null,
						null,
						showLoadDataResultCallback, showErrorCallback);

			} catch (e) {
				showLog("Type: " + AutoScript.getErrorType() + "\nMessage: "
						+ AutoScript.getErrorMessage());
			}
		}

		/**
		 * Funcion para la carga de un fichero. Almacena el contenido del fichero en un campo oculto y muestra su nombre.
		 * LA CARGA INDEPENDIENTE DE FICHEROS DEBE EVITARSE EN LA MEDIDA DE LO POSIBLE. Si deseas firmar, cofirmar o contrafirmar
		 * un fichero, llama al metodo correspondiente (sign(), coSign() o counterSign()) sin indicar los datos.
		 * El uso del metodo de carga no sera compatible con el Cliente movil.
		 */
		function browseFirma(title) {
/* 			try {
				AutoScript.getFileNameContentBase64(
						title,
						"csig,xsig,sig,pdf,xml",
						"Fichero de firma electrónica",
						null,
						showLoadFirmaResultCallback, showErrorCallback);

			} catch (e) {
				showLog("Type: " + AutoScript.getErrorType() + "\nMessage: "
						+ AutoScript.getErrorMessage());
			} */
			
			
			
			try {
				AutoScript.getMultiFileNameContentBase64(
						title,
						"csig,xsig,sig,pdf,xml",
						"Fichero de firma electrónica",
						null,
						showLoadFirmasResultCallback, showErrorCallback);

			} catch (e) {
				showLog("Type: " + AutoScript.getErrorType() + "\nMessage: "
						+ AutoScript.getErrorMessage());
			}
		}

		function showLoadDataResultCallback(fileName, dataB64) {

			dataFilename.innerHTML = fileName;
			data.value = dataB64;
		}
		
		
		
		
		
		function showLoadFirmasResultCallback(fileNames, datasB64) {

			var buffer = "";
			for (var i = 0; i < fileNames.length; i++) {
				buffer += fileNames[i] + ": " + datasB64[i] + "\n";
			}
			showLog(buffer);
		}
		
		
		
		
		

		function showLoadFirmaResultCallback(fileName, dataB64) {

			signatureFilename.innerHTML = fileName;
			signature.value = dataB64;

		}

		function setStickySignature() {

			var isSticky = document.getElementById("sticky").checked;

			AutoScript.setStickySignatory(isSticky);

		}

		function cleanDataField(dataField, textDiv) {

			textDiv.innerHTML = "";
			dataField.value = null;
		}

		function addExtraParam(extraParam) {
			var paramsList = document.getElementById("params");
			paramsList.value = paramsList.value + "\n" + extraParam;
			document.getElementById('newParam').value = "";
		}

		function cleanExtraParams() {
			document.getElementById("params").value = "";
			document.getElementById('newParam').value = "";
		}

		function showLog(newLog) {
			document.getElementById('console').value = document
					.getElementById('console').value
					+ "\n" + newLog;
		}
